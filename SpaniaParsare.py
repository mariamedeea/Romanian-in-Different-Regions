import os
import json
from bs4 import BeautifulSoup

def extract_metadata_from_html(file_path):
    """Extract metadata from an HTML file."""
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Title
    title_element = soup.find("meta", property="og:title")
    title = title_element["content"].strip() if title_element else None

    # Content
    content_element = soup.find("div", class_="entry-content")
    content = content_element.get_text(separator="\n").strip() if content_element else None

    # Author
    author_element = soup.find("strong", string="Autor:")
    author = author_element.next_sibling.strip() if author_element else None

    # Date
    date_element = soup.find("time", class_="post-published updated")
    date = date_element["datetime"].strip() if date_element else None

    # Category
    category_element = soup.find("div", class_="term-badges")
    category = (
        category_element.find("a").get_text().strip()
        if category_element and category_element.find("a")
        else None
    )

    # URL
    url_element = soup.find("link", rel="canonical")
    url = url_element["href"].strip() if url_element else None

    # Region
    region = "Spania"

    return {
        "title": title,
        "content": content,
        "author": author,
        "date": date,
        "category": category,
        "url": url,
        "region": region,
    }

def process_html_folder(input_dir, output_file):
    """Process all HTML files in a folder and save metadata to a JSON file."""
    metadata_list = []

    # Iterate through all files in the folder
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".html"):  # Only process HTML files
            file_path = os.path.join(input_dir, file_name)
            metadata = extract_metadata_from_html(file_path)
            metadata_list.append(metadata)
            print(f"Processed: {file_name}")

    # Save metadata to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, ensure_ascii=False, indent=4)
    print(f"Metadata saved to {output_file}")

if __name__ == "__main__":
    # Folder containing HTML files
    INPUT_DIR = "spania_occidentul_articles"  # Replace with the path to your folder
    # Output JSON file
    OUTPUT_FILE = "spania.json"

    # Process all HTML files in the folder
    process_html_folder(INPUT_DIR, OUTPUT_FILE)
