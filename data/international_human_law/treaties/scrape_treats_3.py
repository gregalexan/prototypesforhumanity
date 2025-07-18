from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

URL = "https://ihl-databases.icrc.org/en/ihl-treaties/historical-treaties-and-documents"
OUTPUT_FILE = "treaties_3.txt"

options = Options()
# options.add_argument('--headless')  # enable if needed
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

def write_titles(titles):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for t in titles:
            f.write(t.strip() + "\n")
    print(f"✅ Saved {len(titles)} historical treaty titles to {OUTPUT_FILE}")

def scrape_treaty_titles():
    driver.get(URL)
    time.sleep(5)

    try:
        container = driver.find_element(By.CSS_SELECTOR, "div.treaty-list.m30")
        a_tags = container.find_elements(By.TAG_NAME, "a")
        titles = [a.text.strip() for a in a_tags if a.text.strip()]
        write_titles(titles)
    except Exception as e:
        print(f"✘ Error: {e}")

    driver.quit()

if __name__ == "__main__":
    scrape_treaty_titles()
