from bs4 import BeautifulSoup

INPUT_FILE = "all_national.html"
OUTPUT_FILE = "all_national_titles.txt"

def extract_titles():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    a_tags = soup.select("a.national-practice-list_title")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for a in a_tags:
            title = a.get_text(strip=True)
            if title:
                f.write(title + "\n")

    print(f"✅ Extracted {len(a_tags)} titles to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_titles()
