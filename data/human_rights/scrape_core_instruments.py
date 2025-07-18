# local_scrape_ohchr.py
from bs4 import BeautifulSoup
import os

INPUT_HTML = "core.html"  # το αποθηκευμένο αρχείο HTML
BASE_URL = "https://www.ohchr.org"
OUT_DIR = "./"

def extract_links_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    links = []
    for a in soup.select(".field__item a[href^='/en/instruments-mechanisms/instruments/']"):
        href = a['href']
        full_url = BASE_URL + href
        title = a.get_text(strip=True)
        links.append((title, full_url))

    return links

def save_links_to_txt(links, out_file):
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        for title, url in links:
            f.write(f"{title}\n{url}\n\n")
    print(f"💾 Saved {len(links)} links to {out_file}")

def main():
    links = extract_links_from_html(INPUT_HTML)
    save_links_to_txt(links, os.path.join(OUT_DIR, "core_instruments_list.txt"))

if __name__ == "__main__":
    main()
