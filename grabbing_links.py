import re
import requests
from bs4 import BeautifulSoup

def get_pmc_ids(url):
    # Make a GET request to the webpage
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the anchor tags (links) in the HTML
    links = soup.find_all("a")

    # Extract the href attribute from each anchor tag
    link_urls = [link.get("href") for link in links]

    # Filter out None values and remove duplicates
    link_urls = list(filter(None, link_urls))
    link_urls = list(set(link_urls))

    # Extract the PMC IDs from the link URLs
    pattern = r"/pmc/articles/([^/]+)/"
    pmc_ids = list(set([re.search(pattern, link).group(1) for link in link_urls if re.match(pattern, link)]))

    # Return the unique PMC IDs
    return pmc_ids
