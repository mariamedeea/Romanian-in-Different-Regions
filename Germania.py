import os
import requests
from bs4 import BeautifulSoup
from time import sleep

def create_directory(dir_name):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def get_html(url):
    """Fetch the HTML content of a page."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_article_links(page_html):
    """Extract article links from a page."""
    soup = BeautifulSoup(page_html, "html.parser")
    articles = soup.find_all("h2", class_="blog-entry-title entry-title")  # Match the <h2> tag with specific class
    links = [a.find("a")["href"] for a in articles if a.find("a")]
    return links

def save_html(content, file_path):
    """Save HTML content to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def download_articles(base_url, output_dir, max_pages=10):
    """Crawl pages and save articles."""
    create_directory(output_dir)
    page = 1

    while page <= max_pages:
        print(f"Fetching page {page}...")
        url = f"{base_url}/page/{page}/"  # Adjust pagination URL
        page_html = get_html(url)

        if not page_html:
            print(f"Skipping page {page}.")
            break

        article_links = parse_article_links(page_html)
        if not article_links:
            print(f"No articles found on page {page}. Ending crawl.")
            break

        for article_url in article_links:
            article_id = article_url.split("/")[-2]  # Extract a unique ID from the URL
            file_name = f"{article_id}.html"
            file_path = os.path.join(output_dir, file_name)

            # Skip if the file already exists
            if os.path.exists(file_path):
                print(f"Article already exists, skipping: {file_name}")
                continue

            article_html = get_html(article_url)
            if article_html:
                save_html(article_html, file_path)
                print(f"Saved article: {file_name}")
            sleep(1)  # Delay to avoid overwhelming the server

        page += 1

if __name__ == "__main__":
    BASE_URL = "https://ziarulromanesc.de"
    OUTPUT_DIR = "germania_ziarulromanesc_de_articles"
    MAX_PAGES = 40  # Adjust the number of pages to crawl

    download_articles(BASE_URL, OUTPUT_DIR, MAX_PAGES)
