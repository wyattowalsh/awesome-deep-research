import asyncio
import csv
import re
import sys
from typing import Dict, List, NoReturn

from loguru import logger
from rich.console import Console

from scripts.update_stars import update_csv_with_stars

# Initialize Rich console
console = Console( record=True )


def extract_main_link( links: str ) -> str:
    """Extract the main link (GitHub or Website) from links string.
    
    Args:
        links: String containing markdown links
        
    Returns:
        str: The first GitHub link or first link found
    """
    # Split links and clean them
    link_list = [ link.strip() for link in links.split( ',' ) ]

    # First try to find a GitHub link
    for link in link_list:
        if 'github.com' in link.lower():
            return link.strip()

    # If no GitHub link, return the first link
    return link_list[ 0 ] if link_list else ''


def clean_html_formatting( text: str ) -> str:
    """Clean HTML formatting from text while preserving markdown.
    
    Args:
        text: Text that may contain HTML formatting
        
    Returns:
        str: Text with HTML formatting removed
    """
    # Replace <br> with newlines
    text = text.replace( '<br>', ' | ' )
    # Remove other HTML tags
    text = re.sub( r'<[^>]+>', '', text )
    return text


def process_row( row: Dict[ str, str ] ) -> Dict[ str, str ]:
    """Process a row to make name clickable and clean formatting.
    
    Args:
        row: Dictionary containing row data
        
    Returns:
        Dict[str, str]: Processed row
    """
    # Extract main link and make name clickable
    if 'links' in row and row[ 'links' ]:
        main_link = extract_main_link( row[ 'links' ] )
        if main_link and 'name' in row:
            row[ 'name' ] = f"{main_link.replace(row['name'], row['name'])}"

    # Clean HTML formatting from all fields
    for key in row:
        if isinstance( row[ key ], str ):
            row[ key ] = clean_html_formatting( row[ key ] )

    return row


def csv_to_md_table( csv_file: str ) -> str:
    """Convert CSV to markdown table with proper formatting.
    
    Args:
        csv_file: Path to the CSV file
        
    Returns:
        str: Formatted markdown table
    """
    with open( csv_file, 'r' ) as f:
        reader = csv.DictReader( f )
        rows = [ process_row( row ) for row in reader ]
        headers = reader.fieldnames or []

        # Create header row
        header_row = "| " + " | ".join( headers ) + " |"
        # Create alignment row
        align_row = "|" + "|".join( [ ":---:" for _ in headers ] ) + "|"
        # Create data rows
        data_rows = []
        for row in rows:
            # Ensure all headers are present
            row_data = [ row.get( header, '' ) for header in headers ]
            data_rows.append( "| " + " | ".join( row_data ) + " |" )

        # Combine all parts with proper newlines
        if data_rows:
            return header_row + "\n" + align_row + "\n" + "\n".join(
                data_rows ) + "\n"
        else:
            return header_row + "\n" + align_row + "\n"


def update_readme_table( readme_file: str, csv_file: str ) -> None:
    """Update the table section in README while preserving other content.
    
    Args:
        readme_file: Path to the README.md file
        csv_file: Path to the CSV file containing table data
    """
    logger.info( "Reading current README file." )
    # Read current README
    with open( readme_file, 'r' ) as f:
        content = f.read()

    logger.info( "Generating new table from CSV." )
    # Generate new table
    table = csv_to_md_table( csv_file )

    # Define the section markers
    start_marker = "## 📊 Data Table"
    end_marker = r"\* Free for local LLM usage"

    # Create the pattern to match the entire section including the table
    pattern = f"({start_marker}.*?){end_marker}"

    logger.info( "Updating README with new table." )
    # Replace the old table section with the new one
    new_content = re.sub( pattern,
                          f"{start_marker}\n\n{table}\n{end_marker}",
                          content,
                          flags=re.DOTALL )

    # Write updated content back to README
    with open( readme_file, 'w' ) as f:
        f.write( new_content )
    logger.info( "README file updated successfully." )


async def main() -> None:
    """Main function to update both star counts and README."""
    try:
        # Configure logging
        logger.remove()                                                        # Remove default handler
        logger.add( "logs/update_readme.log",
                    rotation="1 MB",
                    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
                    level="INFO" )
        logger.add( sys.stderr, level="INFO" )                                 # Add console output

        # First update star counts
        logger.info( "Updating GitHub star counts..." )
        await update_csv_with_stars()

        # Then update README
        logger.info( "Updating README table..." )
        update_readme_table( 'README.md', 'table.csv' )

        logger.info( "All updates completed successfully" )
    except FileNotFoundError as e:
        logger.error( f"File not found: {e}" )
        raise
    except PermissionError as e:
        logger.error( f"Permission error: {e}" )
        raise
    except Exception as e:
        logger.error( f"Unexpected error: {e}" )
        raise


def run() -> NoReturn:
    """Entry point for the script."""
    try:
        asyncio.run( main() )
        sys.exit( 0 )
    except Exception:
        sys.exit( 1 )


if __name__ == '__main__':
    run()
