import requests
import pdfplumber
import re
from io import BytesIO

# Step 1: Download the PDF
print("📥 Downloading UN Charter PDF...")
url = "https://treaties.un.org/doc/publication/ctc/uncharter.pdf"
response = requests.get(url)
response.raise_for_status()

# Step 2: Load PDF and extract text
print("📄 Extracting text from PDF...")
pdf = pdfplumber.open(BytesIO(response.content))
text = "\n\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
pdf.close()

# Step 3: Split text into articles using regex
print("🔍 Parsing articles...")
article_pattern = re.compile(r'(Article [IVXLCDM0-9]+)\s*\n', re.IGNORECASE)
parts = article_pattern.split(text)

if len(parts) < 2:
    raise ValueError("⚠️ No articles found. Check regex or PDF formatting.")

# Step 4: Save to .txt file
print("💾 Saving to 'un_charter_articles.txt'...")
with open("un_charter_articles.txt", "w", encoding="utf-8") as f:
    # First part is likely the Preamble + Chapter headings
    f.write(parts[0].strip() + "\n\n")
    # Remaining parts are article pairs: (title, body)
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ''
        f.write(title + "\n")
        f.write(body + "\n\n")

print("✅ Done: UN Charter saved to 'un_charter_articles.txt'")
