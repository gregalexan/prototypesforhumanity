from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

HTML_FILE = "national.html"
BASE_URL = "https://ihl-databases.icrc.org"
OUTPUT_FILE = "national_implementation.txt"

options = Options()
# options.add_argument('--headless')  # Enable after debugging
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

def write_to_file(title, body):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"## {title.strip()}\n\n{body.strip()}\n\n")
        f.flush()

def extract_links_from_html():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    a_tags = soup.select("div.national-practice-list_item a.national-practice-list_title")
    links = [BASE_URL + a['href'] for a in a_tags if a.get('href')]
    return links

def scrape_national_pages(links):
    for url in links:
        try:
            print(f"➡ Visiting: {url}")
            driver.get(url)
            time.sleep(3)

            content = driver.find_element(By.CSS_SELECTOR, "div.national-practice__content-main")
            title = content.find_element(By.TAG_NAME, "h1").text
            body = content.text

            write_to_file(title, body)
            print(f"✔ Saved: {title}")
        except Exception as e:
            print(f"✘ Error on {url}: {e}")

    driver.quit()
    print(f"\n✅ All content written to {OUTPUT_FILE}")

if __name__ == "__main__":
    links = extract_links_from_html()
    print(f"🔗 Found {len(links)} links.")
    scrape_national_pages(links)
