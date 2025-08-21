from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def extract_internal_links(file_path, base_url):
    """Extract internal links from the saved HTML file."""
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    domain = urlparse(base_url).netloc
    links = set()
    links.add(base_url)  # Include the main URL

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        absolute_url = urljoin(base_url, href)  # Convert relative URLs to absolute
        parsed_url = urlparse(absolute_url)

        if parsed_url.netloc == domain and absolute_url.startswith("http"):
            links.add(absolute_url)

    print(f"Extracted {len(links)} internal links.")
    return links
