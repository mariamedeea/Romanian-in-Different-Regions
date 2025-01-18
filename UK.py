import os
import requests
from bs4 import BeautifulSoup
from time import sleep

def create_directory(dir_name):
    """Creează un director dacă nu există deja."""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def get_html(url):
    """Obține conținutul HTML al unei pagini."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_article_links(page_html):
    """Extrage link-urile articolelor dintr-o pagină."""
    soup = BeautifulSoup(page_html, "html.parser")
    articles = soup.find_all("h3", class_="g1-gamma g1-gamma-1st entry-title")
    links = [a.find("a")["href"] for a in articles if a.find("a")]
    return links

def save_html(content, file_path):
    """Salvează HTML-ul într-un fișier."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def download_articles(base_url, output_dir, max_pages=10):
    """Crawlează paginile și salvează articolele."""
    create_directory(output_dir)
    page = 1

    while page <= max_pages:
        print(f"Fetching page {page}...")
        url = f"{base_url}/page/{page}/"
        page_html = get_html(url)

        if not page_html:
            print(f"Skipping page {page}.")
            break

        article_links = parse_article_links(page_html)
        if not article_links:
            print(f"No articles found on page {page}. Ending crawl.")
            break

        for article_url in article_links:
            article_html = get_html(article_url)
            if article_html:
                article_id = article_url.split("/")[-2]
                file_name = f"{article_id}.html"
                file_path = os.path.join(output_dir, file_name)

                # Skip if the file already exists
                if os.path.exists(file_path):
                    print(f"Article already exists, skipping: {file_name}")
                    continue

                save_html(article_html, file_path)
                print(f"Saved article: {file_name}")
            sleep(1)  # Delay to avoid overwhelming the server

        page += 1

if __name__ == "__main__":
    BASE_URL = "https://ziarulromanesc.net"
    OUTPUT_DIR = "UK_ziarulromanesc_articles"
    MAX_PAGES = 200  # Numărul de pagini de știri de descărcat

    download_articles(BASE_URL, OUTPUT_DIR, MAX_PAGES)
