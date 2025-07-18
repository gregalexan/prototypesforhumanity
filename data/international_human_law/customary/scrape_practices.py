from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

BASE_URL = "https://ihl-databases.icrc.org/en/customary-ihl/v2"
OUTPUT_FILE = "customary_practice.txt"

options = Options()
# options.add_argument('--headless')  # uncomment after debugging
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

def write_to_file(title, body):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"## {title.strip()}\n\n{body.strip()}\n\n")
        f.flush()

def scrape_practice_rules():
    driver.get(BASE_URL)
    time.sleep(5)

    print("🔍 Loading sections from v2...")
    sections = driver.find_elements(By.CSS_SELECTOR, "div.customary-practice__section")
    print(f"📦 Found {len(sections)} sections.")

    links = []
    for section in sections:
        anchors = section.find_elements(By.CSS_SELECTOR, "a.style_wrap__4L4An")
        for a in anchors:
            href = a.get_attribute("href")
            if href and "/en/customary-ihl/v2/" in href:
                links.append(href)

    print(f"🔗 Total rule links found: {len(links)}")

    visited = set()
    for url in links:
        if url in visited:
            continue
        visited.add(url)
        try:
            print(f"➡ Visiting: {url}")
            driver.get(url)
            time.sleep(2)

            main = driver.find_element(By.CSS_SELECTOR, "div.customary-practice__content-main")
            title = main.find_element(By.CSS_SELECTOR, "h1.customary-practice__content-title").text
            body = main.text

            write_to_file(title, body)
            print(f"✔ Scraped: {title}")
        except Exception as e:
            print(f"✘ Error scraping {url}: {e}")

    driver.quit()
    print(f"\n✅ All content saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_practice_rules()
