import re
import json
from PyPDF2 import PdfReader

def extract_articles_from_pdf(pdf_path):
    # Διαβάζουμε το PDF
    reader = PdfReader(pdf_path)
    text = "\n".join([page.extract_text() for page in reader.pages])

    # Διαχωρισμός ανά άρθρο
    article_blocks = re.split(r"\nΑ[ρΡ]θρο:\s*(\d+)", text)

    # Δομημένα blocks: (αριθμός άρθρου, περιεχόμενο)
    structured_blocks = []
    for i in range(1, len(article_blocks), 2):
        article_number = article_blocks[i].strip()
        content = article_blocks[i + 1].strip()
        structured_blocks.append((article_number, content))

    # Μετατροπή κάθε block σε JSON object
    articles = []
    for number, block in structured_blocks:
        # Ανίχνευση πεδίων
        date_match = re.search(r"Ημ/νία:\s*(\d{2}.\d{2}.\d{4})", block)
        valid_from_match = re.search(r"Ημ/νία Ισχύος:\s*(\d{2}.\d{2}.\d{4})", block)
        thesaurus_match = re.search(r"Περιγραφή όρου θησαυρού:\s*(.*?)\n", block)
        title_match = re.search(r"Τίτλος Αρθρου\s*(.*?)\n", block)
        lemmas_match = re.search(r"Λήμματα\s*(.*?)\n", block)
        text_match = re.search(r"Κείμενο Αρθρου\s*(.+)", block, re.DOTALL)

        articles.append({
            "title": "Αστικός Κώδικας",
            "article_number": number,
            "date": date_match.group(1) if date_match else None,
            "valid_from": valid_from_match.group(1) if valid_from_match else None,
            "thesaurus_description": thesaurus_match.group(1).strip() if thesaurus_match else None,
            "headline": title_match.group(1).strip() if title_match else None,
            "lemmas": [lemma.strip() for lemma in lemmas_match.group(1).split(",")] if lemmas_match else [],
            "content": text_match.group(1).strip() if text_match else block.strip()
        })

    return articles

if __name__ == "__main__":
    pdf_path = "Αστικός-Κώδικας.pdf"  # ή δώσε την απόλυτη διαδρομή
    output_json = "astikos_kodikas_structured.json"

    articles = extract_articles_from_pdf(pdf_path)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Εξήχθησαν {len(articles)} άρθρα και αποθηκεύτηκαν στο '{output_json}'")
