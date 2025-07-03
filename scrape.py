import requests
from bs4 import BeautifulSoup
import time

BASE_ARTICLE_URL = "https://www.hellenicparliament.gr/Vouli-ton-Ellinon/To-Politevma/Syntagma/article-{}/"
MAX_ARTICLES = 124  # Πραγματικός αριθμός άρθρων
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_article(number):
    url = BASE_ARTICLE_URL.format(number)
    res = requests.get(url, headers=HEADERS)
    res.encoding = 'utf-8'

    if res.status_code != 200:
        print(f"❌ Άρθρο {number}: Δεν βρέθηκε (HTTP {res.status_code})")
        return None

    soup = BeautifulSoup(res.text, 'html.parser')
    content_div = soup.find("div", class_="pagecontent")
    if not content_div:
        print(f"⚠️ Άρθρο {number}: Δεν βρέθηκε το περιεχόμενο.")
        return None

    text = content_div.get_text(separator="\n", strip=True)
    return text

def save_articles():
    with open("syntagma_final.txt", "w", encoding="utf-8") as f:
        for i in range(1, MAX_ARTICLES + 1):
            content = fetch_article(i)
            if content:
                f.write(f"Άρθρο {i}\n")
                f.write(content + "\n")
                f.write("=" * 60 + "\n")
                print(f"✅ Άρθρο {i} OK")
            else:
                print(f"⛔ Άρθρο {i} skipped")
            time.sleep(0.5)  # μικρό delay για να είμαστε ευγενικοί με τον server

if __name__ == "__main__":
    save_articles()
