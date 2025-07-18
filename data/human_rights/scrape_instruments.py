import os
import time
import re
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

IN_FILE = "instruments_list.txt"
OUT_DIR = "instrument_texts"
os.makedirs(OUT_DIR, exist_ok=True)

driver = uc.Chrome(headless=False)

def clean_title(full_title):
    # Αφαιρεί το "Adopted DD MMM YYYY"
    return re.sub(r"^Adopted \d{1,2} \w{3} \d{4}", "", full_title).strip()

def make_safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip().replace(" ", "_")[:100]

def save_instrument(name, url):
    try:
        print(f"🔸 Visiting {name}")
        driver.get(url)
        time.sleep(8)  # περιμένουμε αρκετά για να περάσει το JS challenge

        soup = BeautifulSoup(driver.page_source, "html.parser")
        main = soup.find("main") or soup
        content = main.get_text(separator="\n", strip=True)

        clean_name = clean_title(name)
        safe_name = make_safe_filename(clean_name)
        filepath = os.path.join(OUT_DIR, f"{safe_name}.txt")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{name}\n{url}\n\n{content}")

        print(f"✅ Saved: {filepath}")
    except Exception as e:
        print(f"❌ Failed for {name}: {e}")

def main():
    with open(IN_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    instruments = [(lines[i], lines[i+1]) for i in range(0, len(lines)-1, 2)]

    print(f"🔍 Starting scraping for {len(instruments)} instruments.")
    for title, link in instruments:
        save_instrument(title, link)

    driver.quit()
    print("✅ Done.")

if __name__ == "__main__":
    main()
