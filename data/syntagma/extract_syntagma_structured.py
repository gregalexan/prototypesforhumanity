import pdfplumber
import re
import json

def extract_syntagma_structured(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i >= 19:  # Παράκαμψη περιεχομένων, τίτλων, προλόγων
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    # Καθαρισμός: ενώνει λέξεις που κόβονται με '-', καθαρίζει κενές γραμμές
    text = re.sub(r"(?<=\S)-\n(?=\S)", "", text)  # π.χ. πρoσω- \n πικότητα => πρoσωπικότητα
    text = re.sub(r"\n+", "\n", text)

    # Βρες άρθρα με βάση "Άρθρο 1", "Άρθρο 5Α", "Άρθρο 117" κ.λπ.
    pattern = r"(Άρθρ[οoOΟ]\s*\d+[Α-Ω]?)"
    splits = re.split(pattern, text)

    articles = []
    for i in range(1, len(splits), 2):
        article_number = splits[i].strip().replace("Άρθρο", "").replace("Άρθρo", "").strip()
        content_block = splits[i + 1].strip()

        # Ομαδοποίηση αριθμημένων παραγράφων: 1. ... 2. ... 3. ...
        numbered_paragraphs = re.findall(r"(?:(?:\*\*)?\d+\.\s+.*?)(?=(?:\*\*)?\d+\.\s+|$)", content_block, re.DOTALL)
        content = "\n".join(p.strip() for p in numbered_paragraphs).strip()

        if not content:
            content = content_block.strip()

        # Ειδικός καθαρισμός για Άρθρο 120 (τελευταίο άρθρο του Συντάγματος)
        if article_number == "120":
            content = re.split(r"(Αθήνα|Ο ΠΡΟΕΔΡΟΣ|Σημειώσεις|ΘΕΜΑΤΙΚΟ ΕΥΡΕΤΗΡΙΟ)", content)[0].strip()
            
        articles.append({
            "title": "Σύνταγμα Ελλάδας",
            "article_number": article_number,
            "content": content
        })

    return articles

if __name__ == "__main__":
    pdf_path = "syntagma1_1.pdf"  # ή δώσε το path στο PDF
    output_json = "syntagma_structured.txt"

    articles = extract_syntagma_structured(pdf_path)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Εξήχθησαν {len(articles)} άρθρα και αποθηκεύτηκαν στο '{output_json}'")
