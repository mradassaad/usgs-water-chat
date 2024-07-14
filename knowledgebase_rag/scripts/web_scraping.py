import requests
from bs4 import BeautifulSoup
import os
import datetime

# Define the base URL
base_url = "https://waterservices.usgs.gov/docs/"

# Function to scrape a webpage and save it as an HTML file
def scrape_page(url, output_dir):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the HTML content as a file
    # Extract the page title
    title = soup.title.string.strip()
    
    # Generate the timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Create the filename
    filename = f"{title}_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(str(soup))
    
    print(f"Scraped {url} and saved as {filepath}")

# Scrape the base URL
scrape_page(base_url, "data/html")

# Scrape child pages
response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")
child_pages = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href is not None and href.startswith("/docs/"):
        child_pages.append("https://waterservices.usgs.gov" + href)

for page in child_pages:
    scrape_page(page, "data/html")