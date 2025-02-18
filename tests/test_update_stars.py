import os
from unittest.mock import AsyncMock, mock_open, patch

import pytest
from aiohttp import ClientError, ClientSession
from loguru import logger

from scripts.update_stars import (
    extract_github_info,
    get_repo_stars,
    process_row,
    update_csv_with_stars,
)

# Test data
SAMPLE_GITHUB_URL = "https://github.com/owner/repo"
SAMPLE_CSV_ROW = {
    "name": "Test Tool",
    "links":
    "[GitHub](https://github.com/owner/repo), [Docs](https://docs.com)"
}
SAMPLE_CSV_CONTENT = """name,links,github_stars
Test Tool,[GitHub](https://github.com/owner/repo),0
"""


@pytest.fixture( autouse=True )
def mock_env_vars():
    """Mock environment variables for all tests."""
    with patch.dict( os.environ, { "GITHUB_TOKEN": "test_token" } ):
        yield


@pytest.fixture
def mock_logger():
    """Mock logger for testing log messages."""
    with patch.object(logger, 'warning') as mock_warn, \
         patch.object(logger, 'error') as mock_error, \
         patch.object(logger, 'info') as mock_info:
        yield { 'warning': mock_warn, 'error': mock_error, 'info': mock_info }


@pytest.mark.asyncio
async def test_extract_github_info():
    # Test valid GitHub URL
    result = await extract_github_info( SAMPLE_GITHUB_URL )
    assert result == ( "owner", "repo" )

    # Test invalid GitHub URL
    result = await extract_github_info( "https://example.com" )
    assert result is None

    # Test malformed URL
    result = await extract_github_info( "https://github.com/invalid" )
    assert result is None

    # Test empty URL
    result = await extract_github_info( "" )
    assert result is None

    # Test None URL
    result = await extract_github_info( None )
    assert result is None


@pytest.mark.asyncio
async def test_get_repo_stars( mock_logger ):
    mock_session = AsyncMock( spec=ClientSession )
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock( return_value={ "stargazers_count": 100 } )

    # Set up the context manager mock properly
    context_manager = AsyncMock()
    context_manager.__aenter__.return_value = mock_response
    mock_session.get.return_value = context_manager

    # Test successful response
    result = await get_repo_stars( mock_session, "owner", "repo" )
    assert result == 100

    # Test failed response
    mock_response.status = 404
    result = await get_repo_stars( mock_session, "owner", "repo" )
    assert result is None
    mock_logger[ 'warning' ].assert_called_once()

    # Test network error
    mock_session.get.side_effect = ClientError( "Network error" )
    result = await get_repo_stars( mock_session, "owner", "repo" )
    assert result is None
    mock_logger[ 'error' ].assert_called_once()

    # Test malformed response
    mock_session.get.side_effect = None
    mock_response.status = 200
    mock_response.json = AsyncMock( return_value={} )
    result = await get_repo_stars( mock_session, "owner", "repo" )
    assert result is None


@pytest.mark.asyncio
async def test_process_row():
    mock_session = AsyncMock( spec=ClientSession )
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock( return_value={ "stargazers_count": 100 } )

    # Set up the context manager mock properly
    context_manager = AsyncMock()
    context_manager.__aenter__.return_value = mock_response
    mock_session.get.return_value = context_manager

    # Test row with GitHub link
    result = await process_row( mock_session, SAMPLE_CSV_ROW.copy() )
    assert result[ "github_stars" ] == "100"

    # Test row without GitHub link
    row_no_github = { "name": "Test", "links": "[Docs](https://docs.com)" }
    result = await process_row( mock_session, row_no_github )
    assert result[ "github_stars" ] == "N/A"

    # Test row with invalid GitHub link
    row_invalid = {
        "name": "Test",
        "links": "[GitHub](https://github.com/invalid)"
    }
    result = await process_row( mock_session, row_invalid )
    assert result[ "github_stars" ] == "N/A"

    # Test row with multiple links including GitHub
    row_multiple = {
        "name":
        "Test",
        "links":
        "[Docs](https://docs.com), [GitHub](https://github.com/owner/repo), [Website](https://example.com)"
    }
    result = await process_row( mock_session, row_multiple )
    assert result[ "github_stars" ] == "100"

    # Test row with no links field
    row_no_links = { "name": "Test" }
    result = await process_row( mock_session, row_no_links )
    assert result[ "github_stars" ] == "N/A"

    # Test row with empty links field
    row_empty_links = { "name": "Test", "links": "" }
    result = await process_row( mock_session, row_empty_links )
    assert result[ "github_stars" ] == "N/A"


@pytest.mark.asyncio
async def test_update_csv_with_stars( tmp_path, mock_logger ):
    # Create temporary CSV file
    csv_file = tmp_path / "test.csv"
    csv_file.write_text( SAMPLE_CSV_CONTENT )

    # Mock aiohttp.ClientSession
    mock_session = AsyncMock( spec=ClientSession )
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock( return_value={ "stargazers_count": 100 } )

    # Set up the context manager mock properly
    context_manager = AsyncMock()
    context_manager.__aenter__.return_value = mock_response
    mock_session.get.return_value = context_manager

    with patch( "aiohttp.ClientSession", return_value=mock_session ):
        await update_csv_with_stars( str( csv_file ) )

    # Verify the updated content
    updated_content = csv_file.read_text()
    assert "100" in updated_content
    mock_logger[ 'info' ].assert_called_once()

    # Test with empty CSV
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text( "name,links,github_stars\n" )

    with patch( "aiohttp.ClientSession", return_value=mock_session ):
        await update_csv_with_stars( str( empty_csv ) )

    # Verify empty CSV handling
    empty_content = empty_csv.read_text()
    assert "name,links,github_stars" in empty_content


@pytest.mark.asyncio
async def test_update_csv_with_stars_file_not_found():
    with pytest.raises( FileNotFoundError ):
        await update_csv_with_stars( "nonexistent.csv" )


@pytest.mark.asyncio
async def test_update_csv_with_stars_permission_error( tmp_path ):
    # Create temporary CSV file without write permissions
    csv_file = tmp_path / "test.csv"
    csv_file.write_text( SAMPLE_CSV_CONTENT )
    os.chmod( csv_file, 0o444 ) # Read-only

    with pytest.raises( PermissionError ):
        await update_csv_with_stars( str( csv_file ) )


@pytest.mark.asyncio
async def test_update_csv_with_stars_no_token( mock_logger ):
    with patch.dict( os.environ, {}, clear=True ):
        # Create temporary CSV file
        csv_file = "table.csv"

        with patch( "builtins.open",
                    mock_open( read_data=SAMPLE_CSV_CONTENT ) ):
            await update_csv_with_stars( csv_file )

        mock_logger[ 'warning' ].assert_called_with(
            "No GITHUB_TOKEN found in environment variables" )
