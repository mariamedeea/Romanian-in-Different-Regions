import os
import json
from bs4 import BeautifulSoup

def extract_metadata_from_file(file_path):
    """Extract metadata from an HTML file."""
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Title
    title_element = soup.find("meta", property="og:title")
    title = title_element["content"].strip() if title_element else None

    # Text content
    article_content = soup.find("div", class_="nv-content-wrap entry-content")

    # Remove all <b> tags from the article content
    if article_content:
        for bold_tag in article_content.find_all("b"):
            bold_tag.decompose()
        text = article_content.get_text(separator="\n").strip()
    else:
        text = None

    # Remove unwanted parts from the text dynamically
    if text:
        # Remove lines containing dates and "ACTUALIZAT" patterns
        cleaned_lines = []
        for line in text.splitlines():
            if not ("ACTUALIZAT" in line or any(char.isdigit() for char in line[:10])):
                cleaned_lines.append(line)
        text = "\n".join(cleaned_lines).strip()

    # Region (specific to this site)
    region = "Germania"

    # Author
    author_element = soup.find("span", class_="author-name fn")
    author = author_element.get_text().strip() if author_element else None

    # Date of publication
    date_element = soup.find("div", style="border-top:1px solid #dedede;border-bottom:1px solid #dedede; font-size:13px;")
    date = None
    if date_element:
        raw_date = date_element.get_text(separator=" ").strip()
        date = raw_date.split(" ")[0] if raw_date else None

    # Category
    category_element = soup.find("a", rel="category tag")
    category = category_element.get_text().strip() if category_element else None

    # URL
    canonical_link = soup.find("link", rel="canonical")
    url = canonical_link["href"] if canonical_link else None

    return {
        "title": title,
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
    INPUT_DIR = "germania_ziarulromanesc_de_articles"  # Replace with the actual directory path
    # Output JSON file
    OUTPUT_FILE = "germania.json"

    process_directory(INPUT_DIR, OUTPUT_FILE)
