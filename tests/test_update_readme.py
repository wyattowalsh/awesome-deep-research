from unittest.mock import AsyncMock, call, mock_open, patch

import pytest
from loguru import logger

from scripts.update_readme import csv_to_md_table, main, run, update_readme_table
from scripts.update_stars import update_csv_with_stars

# Sample CSV content for testing
sample_csv_content = """name,summary,interface
Tool1,Description1,Interface1
Tool2,Description2,Interface2
"""

# Sample README content for testing
sample_readme_content = """# awesome-deep-research

## 📊 Data Table

| name | summary | interface |
|:---:|:---:|:---:|
| Tool1 | Description1 | Interface1 |
| Tool2 | Description2 | Interface2 |

\* Free for local LLM usage
"""

# Additional test case for empty CSV
empty_csv_content = """name,summary,interface\n"""

# Additional test case for malformed CSV
malformed_csv_content = """name,summary,interface
Tool1,Description1
Tool2,Description2,Interface2,ExtraColumn
"""


@pytest.fixture
def mock_logger():
    """Mock logger for testing log messages."""
    with patch.object(logger, 'warning') as mock_warn, \
         patch.object(logger, 'error') as mock_error, \
         patch.object(logger, 'info') as mock_info, \
         patch.object(logger, 'remove') as mock_remove, \
         patch.object(logger, 'add') as mock_add:
        yield {
            'warning': mock_warn,
            'error': mock_error,
            'info': mock_info,
            'remove': mock_remove,
            'add': mock_add
        }


def test_csv_to_md_table_empty():
    with patch( 'builtins.open', mock_open( read_data=empty_csv_content ) ):
        result = csv_to_md_table( 'dummy.csv' )
        expected = """| name | summary | interface |\n|:---:|:---:|:---:|\n"""
        assert result == expected


def test_csv_to_md_table_malformed():
    with patch( 'builtins.open',
                mock_open( read_data=malformed_csv_content ) ):
        result = csv_to_md_table( 'dummy.csv' )
        expected = """| name | summary | interface |\n|:---:|:---:|:---:|\n| Tool1 | Description1 |  |\n| Tool2 | Description2 | Interface2 |\n"""
        assert result == expected


def test_csv_to_md_table():
    with patch( 'builtins.open', mock_open( read_data=sample_csv_content ) ):
        result = csv_to_md_table( 'dummy.csv' )
        expected = """| name | summary | interface |\n|:---:|:---:|:---:|\n| Tool1 | Description1 | Interface1 |\n| Tool2 | Description2 | Interface2 |\n"""
        assert result == expected


def test_csv_to_md_table_file_not_found():
    with pytest.raises( FileNotFoundError ):
        csv_to_md_table( 'nonexistent.csv' )


def test_update_readme_table( mock_logger ):
    with patch( 'builtins.open',
                mock_open( read_data=sample_readme_content ) ) as mocked_file:
        update_readme_table( 'dummy_readme.md', 'dummy.csv' )
        mocked_file().write.assert_called_once_with( sample_readme_content )
        mock_logger[ 'info' ].assert_has_calls( [
            call( "Reading current README file." ),
            call( "Generating new table from CSV." ),
            call( "Updating README with new table." ),
            call( "README file updated successfully." )
        ] )


def test_update_readme_table_no_change( mock_logger ):
    with patch( 'builtins.open',
                mock_open( read_data=sample_readme_content ) ) as mocked_file:
        update_readme_table( 'dummy_readme.md', 'dummy.csv' )
        mocked_file().write.assert_called_once_with( sample_readme_content )
        mock_logger[ 'info' ].assert_has_calls( [
            call( "Reading current README file." ),
            call( "Generating new table from CSV." ),
            call( "Updating README with new table." ),
            call( "README file updated successfully." )
        ] )


def test_update_readme_table_file_not_found( mock_logger ):
    with patch( 'builtins.open',
                mock_open( read_data=sample_readme_content ) ) as mocked_file:
        mocked_file.side_effect = FileNotFoundError( "File not found" )
        with pytest.raises( FileNotFoundError ):
            update_readme_table( 'dummy_readme.md', 'dummy.csv' )
        mock_logger[ 'info' ].assert_called_once_with(
            "Reading current README file." )


def test_update_readme_table_permission_error( mock_logger ):
    with patch( 'builtins.open',
                mock_open( read_data=sample_readme_content ) ) as mocked_file:
        mocked_file.side_effect = PermissionError( "Permission denied" )
        with pytest.raises( PermissionError ):
            update_readme_table( 'dummy_readme.md', 'dummy.csv' )
        mock_logger[ 'info' ].assert_called_once_with(
            "Reading current README file." )


@pytest.mark.asyncio
async def test_main( tmp_path, mock_logger ):
    # Create temporary files
    readme_file = tmp_path / "README.md"
    csv_file = tmp_path / "table.csv"

    readme_file.write_text( sample_readme_content )
    csv_file.write_text( sample_csv_content )

    # Mock update_csv_with_stars
    mock_update_stars = AsyncMock()

    with patch('scripts.update_readme.update_csv_with_stars', mock_update_stars), \
         patch('scripts.update_readme.update_readme_table') as mock_update_table:

        await main()

        # Verify all functions were called
        mock_update_stars.assert_called_once()
        mock_update_table.assert_called_once_with( 'README.md', 'table.csv' )

        # Verify logging setup
        mock_logger[ 'remove' ].assert_called_once()
        assert mock_logger[ 'add' ].call_count >= 2
        mock_logger[ 'info' ].assert_has_calls( [
            call( "Updating GitHub star counts..." ),
            call( "Updating README table..." ),
            call( "All updates completed successfully" )
        ] )


@pytest.mark.asyncio
async def test_main_with_errors( tmp_path, mock_logger ):
    # Test FileNotFoundError
    mock_update_stars = AsyncMock(
        side_effect=FileNotFoundError( "File not found" ) )
    with patch('scripts.update_readme.update_csv_with_stars', mock_update_stars), \
         pytest.raises(FileNotFoundError):
        await main()
        mock_logger[ 'error' ].assert_called_with(
            "File not found: File not found" )

    # Test PermissionError
    mock_update_stars = AsyncMock(
        side_effect=PermissionError( "Permission denied" ) )
    with patch('scripts.update_readme.update_csv_with_stars', mock_update_stars), \
         pytest.raises(PermissionError):
        await main()
        mock_logger[ 'error' ].assert_called_with(
            "Permission error: Permission denied" )

    # Test unexpected error
    mock_update_stars = AsyncMock(
        side_effect=Exception( "Unexpected error" ) )
    with patch('scripts.update_readme.update_csv_with_stars', mock_update_stars), \
         pytest.raises(Exception):
        await main()
        mock_logger[ 'error' ].assert_called_with(
            "Unexpected error: Unexpected error" )


def test_run_success( mock_logger ):
    mock_main = AsyncMock()
    with patch('scripts.update_readme.main', mock_main), \
         patch('sys.exit') as mock_exit:
        run()
        mock_main.assert_called_once()
        mock_exit.assert_called_once_with( 0 )


def test_run_failure( mock_logger ):
    mock_main = AsyncMock( side_effect=Exception( "Test error" ) )
    with patch('scripts.update_readme.main', mock_main), \
         patch('sys.exit') as mock_exit:
        run()
        mock_main.assert_called_once()
        mock_exit.assert_called_once_with( 1 )
