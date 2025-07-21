import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

BASE_URL = "https://www.un.org/en/about-us/un-charter"
OUTPUT_FILE = "un_charter.txt"

chrome_options = Options()
# chrome_options.add_argument("--headless")  # remove comment if you want headless
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)

def get_charter_links():
    print("🔍 Fetching UN Charter links...")
    driver.get(BASE_URL)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    toc = soup.find("ul", id="31857")
    links = []
    if toc:
        for a in toc.find_all("a", href=True):
            title = a.get_text(strip=True)
            href = a["href"]
            full_url = "https://www.un.org" + href if href.startswith("/") else href
            links.append((title, full_url))
    print(f"🔗 Found {len(links)} sections.")
    return links

def extract_correct_div_text(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "col-md-10"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        div = soup.find("div", class_="col-md-10 col-sm-12")
        if div:
            return div.get_text(separator="\n", strip=True)
        else:
            print(f"❌ Target div not found in {url}")
            return ""
    except Exception as e:
        print(f"❌ Error visiting {url}: {e}")
        return ""

def main():
    links = get_charter_links()
    all_text = ""
    for title, url in links:
        print(f"➡️  Visiting {title} | {url}")
        content = extract_correct_div_text(url)
        if content:
            all_text += f"\n\n=== {title} ===\n\n{content}"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(all_text)

    print(f"\n✅ All content saved to {OUTPUT_FILE}")
    driver.quit()

if __name__ == "__main__":
    main()
