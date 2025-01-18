import os
import json
from bs4 import BeautifulSoup

def extract_metadata_from_file(file_path):
    """Extract metadata from an HTML file."""
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Remove unwanted elements
    for element in soup.find_all("div", class_="yasr-custom-text-vv-before yasr-custom-text-vv-before-183689"):
        element.decompose()

    # Extract text content of the article
    article_content = soup.find("div", class_="entry-content")
    text = article_content.get_text(separator="\n").strip() if article_content else None

    # Region (specific to this site)
    region = "Italia"

    # Author
    author_element = soup.find("meta", attrs={"name": "author"})
    author = author_element["content"].strip() if author_element else None

    # Date of publication
    date_element = soup.find("time", class_="entry-date")
    date = date_element.get_text().strip() if date_element else None

    # Category (extract only the text, without "in")
    category = None
    category_element = soup.find("span", class_="entry-categories")
    if category_element:
        actual_category = category_element.find("span", itemprop="articleSection")
        if actual_category:
            category = actual_category.get_text().strip()

    # Title
    title_element = soup.find("meta", property="og:title")
    title = title_element["content"].strip() if title_element else None

    # URL
    canonical_link = soup.find("link", rel="canonical")
    url = canonical_link["href"] if canonical_link else None

    return {
        "title": title,       # New component for the title
        "text": text,
        "region": region,
        "author": author,
        "date": date,
        "category": category,
        "url": url,
    }

def process_directory(input_dir, output_file):
    """Process all HTML files in a directory and save metadata to a JSON file."""
    articles_metadata = []

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".html"):
            file_path = os.path.join(input_dir, file_name)
            metadata = extract_metadata_from_file(file_path)
            articles_metadata.append(metadata)
            print(f"Processed: {file_name}")

    # Save all metadata to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles_metadata, f, ensure_ascii=False, indent=4)
    print(f"Metadata saved to {output_file}")

if __name__ == "__main__":
    # Input directory containing HTML files
    INPUT_DIR = "gazetaromaneasca_articles"  # Replace with your directory path
    # Output JSON file
    OUTPUT_FILE = "italia.json"

    process_directory(INPUT_DIR, OUTPUT_FILE)
