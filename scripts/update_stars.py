import asyncio
import csv
import os
import re
from typing import Dict, List, Optional, Tuple

import aiohttp
from loguru import logger

# Configure logger
logger.add( "logs/update_stars.log", rotation="1 MB" )

GITHUB_TOKEN = os.getenv( "GITHUB_TOKEN" )
if not GITHUB_TOKEN:
    logger.warning( "No GITHUB_TOKEN found in environment variables" )

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else "",
}


async def extract_github_info( url: str ) -> Optional[ Tuple[ str, str ] ]:
    """Extract owner and repo from GitHub URL."""
    if not url or not isinstance( url, str ):
        return None

    github_pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search( github_pattern, url )
    if match:
        return match.group( 1 ), match.group( 2 )
    return None


async def get_repo_stars( session: aiohttp.ClientSession, owner: str,
                          repo: str ) -> Optional[ int ]:
    """Fetch star count for a GitHub repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        async with session.get( url, headers=HEADERS ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get( "stargazers_count" )
            else:
                logger.warning(
                    f"Failed to fetch stars for {owner}/{repo}: {response.status}"
                )
                return None
    except Exception as e:
        logger.error( f"Error fetching stars for {owner}/{repo}: {e}" )
        return None


async def process_row( session: aiohttp.ClientSession,
                       row: Dict[ str, str ] ) -> Dict[ str, str ]:
    """Process a single row from the CSV."""
    links = row.get( "links", "" )
    github_url = None

    # Extract GitHub URL if present
    for url in links.split( "," ):
        if "github.com" in url.lower():
            github_url = url.strip( "[]() " )
            break

    if github_url:
        github_info = await extract_github_info( github_url )
        if github_info:
            owner, repo = github_info
            stars = await get_repo_stars( session, owner, repo )
            if stars is not None:
                row[ "github_stars" ] = str( stars )
            else:
                row[ "github_stars" ] = "N/A"
        else:
            row[ "github_stars" ] = "N/A"
    else:
        row[ "github_stars" ] = "N/A"

    return row


async def update_csv_with_stars( csv_file: str = "table.csv" ) -> None:
    """Update CSV file with GitHub star counts."""
    rows: List[ Dict[ str, str ] ] = []
    fieldnames: List[ str ] = []

    # Read existing CSV
    with open( csv_file, "r" ) as f:
        reader = csv.DictReader( f )
        fieldnames = reader.fieldnames or []
        rows = [ row for row in reader ]

    # Add github_stars to fieldnames if not present
    if "github_stars" not in fieldnames:
        fieldnames.append( "github_stars" )

    # Process all rows
    async with aiohttp.ClientSession() as session:
        tasks = [ process_row( session, row ) for row in rows ]
        updated_rows = await asyncio.gather( *tasks )

    # Write updated CSV
    with open( csv_file, "w", newline="" ) as f:
        writer = csv.DictWriter( f, fieldnames=fieldnames )
        writer.writeheader()
        writer.writerows( updated_rows )

    logger.info( f"Updated {csv_file} with GitHub star counts" )


if __name__ == "__main__":
    asyncio.run( update_csv_with_stars() )
