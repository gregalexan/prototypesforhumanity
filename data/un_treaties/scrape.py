# scrape_un_treaties.py
import requests
from bs4 import BeautifulSoup
import os

BASE_URL = "https://treaties.un.org"
START_URL = BASE_URL + "/Pages/Home.aspx"

def get_treaty_links():
    resp = requests.get(START_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = set()
    for a in soup.select("a"):
        href = a.get("href", "")
        if href.startswith("/Pages/") and "TREATY" in href:
            links.add(BASE_URL + href)
    return list(links)

def download_treaty(url, output_dir="un_treaties"):
    os.makedirs(output_dir, exist_ok=True)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.select_one("h1").get_text(strip=True)
    paragraphs = soup.select("div.TreatyText p")
    text = "\n".join(p.get_text() for p in paragraphs)
    filename = f"{output_dir}/{title[:50].replace(' ','_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{title}\n\n{text}")
    print("Saved", filename)

def main():
    treaty_links = get_treaty_links()
    print(f"Found {len(treaty_links)} treaties.")
    for link in treaty_links[:10]:  # adjust range as needed
        download_treaty(link)

if __name__ == "__main__":
    main()
