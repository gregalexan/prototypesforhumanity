from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

URL = "https://ihl-databases.icrc.org/en/customary-ihl/sources"
OUTPUT_FILE = "customary_sources.txt"

options = Options()
# options.add_argument('--headless')  # uncomment after debug
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

def write_to_file(text):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text.strip())
        f.flush()

def scrape_sources_page():
    driver.get(URL)
    time.sleep(5)

    print(f"🔍 Visiting {URL}")
    try:
        div = driver.find_element(By.CLASS_NAME, "cihl-sources-list_main")
        body = div.text
        write_to_file(body)
        print(f"✅ Content saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"✘ Failed to scrape sources page: {e}")

    driver.quit()

if __name__ == "__main__":
    scrape_sources_page()
