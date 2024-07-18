""" Helper functions for web scraping, Unstructured data processing, embedding calculations, and upserting to Pinecone. """

import os
import requests
from bs4 import BeautifulSoup
import os
import datetime
import logging
from urllib.parse import urlparse

# Function to check if a URL is valid.
def is_valid_url(url: str) -> str:
    """
    Check if a URL is valid. If the URL is not valid, raise a ValueError. 
    
    Args:
        url (str): A URL to check.

    Returns:
        str: A valid URL.
    """

    if url is None:
        logging.warning("URL cannot be None.")
        raise ValueError("URL cannot be None.")
    elif not url.startswith("https://"):
        logging.error("Invalid URL. Please provide a valid URL that starts with https://.")
        raise ValueError("Invalid URL. Please provide a valid URL that starts with https://.")
    elif any(char in url for char in ['<', '>', '"', "'", ';', '(', ')', '&', '|', '`']):
        logging.error(f"Invalid character found in URL.")
        raise ValueError(f"Invalid character found in URL.")
    
    if not url.endswith("/"):
        url += "/"

    return url

# Function to find all pages with the same base URL.
def find_pages_from_base(base_url: str, max_pages: int = 1000) -> list:
    """Find all pages with the same base URL. Uses beautiful soup to scan the base page for child pages.
    This function will recursively scan child pages for more child pages until the max_pages is reached or no new pages are found.

    Args:
        base_url (str): The base URL.
        max_pages (int): A maximum number of hrefs to check. Defaults to 1000.

    Returns:
        list: A list of URLs.
    """

    # TODO: This function rigidely processes relatives URLs which may not work for some websites like https://learn.microsoft.com/en-us/azure/azure-functions/.

    # Check if the URL is valid
    base_url = is_valid_url(base_url)  

    # List to store pages to visit and set to store visited pages
    visited = set()
    to_visit = [base_url]

    def scrape(url):
        # Parse url
        parsed_url = urlparse(url)

        # Send a GET request to the webpage
        page = requests.get(url)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all("a")
        
        for link in links:
            href = link.get("href")

            new_url = None
            # Check if the href is a child page
            if href is not None and (href.startswith(parsed_url.path)):
                new_url = url.replace(parsed_url.path, "") + href
            elif href is not None and (href.startswith(url)):
                new_url = href
            
            # Disregard anchor urls
            if new_url is not None and "#" in new_url:
                new_url = None

            # Check if new URL is valid
            try:
                new_url = is_valid_url(new_url)
            except ValueError as e:
                logging.debug(f"Skipping URL Error: {e}")
                continue

            if new_url is not None and new_url not in visited:
                to_visit.append(new_url)

    i = 0
    while to_visit:
        # increase counter
        i += 1
        logging.debug(f"Visiting URL: {to_visit[0]}")
        # Check if counter is greater than max pages
        if i > max_pages:
            logging.warning(f"Max pages reached: {max_pages}.")
            break
        # Get the next page to visit
        page = to_visit.pop(0)
        if page not in visited:
            visited.add(page)
            scrape(page)

    return list(visited)