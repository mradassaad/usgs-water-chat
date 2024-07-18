""" Helper functions for web scraping, Unstructured data processing, embedding calculations, and upserting to Pinecone. """

import os
import requests
from bs4 import BeautifulSoup
import os
import datetime
import logging
from urllib.parse import urlparse


# Function to find all pages with the same base URL.
def find_pages_from_base(base_url: str, max_pages: int = 1000) -> list:
    """Find all pages with the same base URL. Uses beautiful soup to scan the base page for child pages. Searches only one level of depth/

    Args:
        base_url (str): The base URL.
        max_pages (int): A maximum number of hrefs to check. Defaults to 1000.

    Returns:
        list: A list of URLs.
    """

    # Ensure base_url is a valid URL
    if base_url is None:
        logging.error("URL cannot be None.")
        raise ValueError("URL cannot be None.")
    elif not base_url.startswith("https://"):
        logging.error("Invalid URL. Please provide a valid URL that starts with https://.")
        raise ValueError("Invalid URL. Please provide a valid URL that starts with https://.")
    elif any(char in base_url for char in ['<', '>', '"', "'", ';', '(', ')', '&', '|', '`']):
        logging.error(f"Invalid character found in URL.")
        raise ValueError(f"Invalid character found in URL.")
    elif not base_url.endswith("/"):
        base_url += "/"

    # Parse url
    parsed_url = urlparse(base_url)

    # Send a GET request to the webpage
    page = requests.get(base_url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("a")
    pages = []
    for link in links:
        href = link.get("href")

        # Check if we have reached the maximum number of pages
        if len(pages) >= max_pages:
            logging.warning(f"Max pages reached: {max_pages}.")
            break

        # Check if the href is a child page
        if href is not None and (href.startswith(parsed_url.path)):
            pages.append(base_url.replace(parsed_url.path, "") + href)
        elif href is not None and (href.startswith(base_url)):
            pages.append(href)

        # keep only unique pages
        pages = list(set(pages))

    return pages