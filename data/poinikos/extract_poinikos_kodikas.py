import re
import json
from PyPDF2 import PdfReader

def extract_penal_code_articles_fixed(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = "\n".join([page.extract_text() for page in reader.pages])

    # Διαχωρισμός με βάση "Αρθρο: <αριθμός>"
    article_blocks = re.split(r"\n*Αρθρο:\s*(\d+[Α-Ω]?)\s*", full_text)

    articles = []
    seen_numbers = set()

    for i in range(1, len(article_blocks), 2):
        number = article_blocks[i].strip()
        content_block = article_blocks[i + 1]

        # Απόφυγε διπλές εγγραφές
        if number in seen_numbers:
            continue
        seen_numbers.add(number)

        article_data = {
            "title": "Ποινικός Κώδικας",
            "article_number": number
        }

        # Εξαγωγή structured πεδίων
        date = re.search(r"Ημ/νία:\s*(\d{2}.\d{2}.\d{4})", content_block)
        valid_from = re.search(r"Ημ/νία Ισχύος:\s*(\d{2}.\d{2}.\d{4})", content_block)
        thesaurus = re.search(r"Περιγραφή όρου θησαυρού:\s*(.*?)\n", content_block)
        headline = re.search(r"Τίτλος Αρθρου\s*(.*?)\n", content_block)
        lemmas = re.search(r"Λήμματα\s*(.*?)\n", content_block)
        notes = re.search(r"Σχόλια\s*(.*?)\n(?=Κείμενο Αρθρου|Αρθρο:|\Z)", content_block, re.DOTALL)
        text_match = re.search(r"Κείμενο Αρθρου\s*(.+)", content_block, re.DOTALL)

        # Καθαρισμός & δομή
        article_data["date"] = date.group(1) if date else None
        article_data["valid_from"] = valid_from.group(1) if valid_from else None
        article_data["thesaurus_description"] = thesaurus.group(1).strip() if thesaurus else None
        article_data["headline"] = headline.group(1).strip() if headline else None
        article_data["lemmas"] = [l.strip() for l in lemmas.group(1).split(",")] if lemmas else []
        article_data["notes"] = notes.group(1).strip() if notes else None
        article_data["content"] = text_match.group(1).strip() if text_match else content_block.strip()

        articles.append(article_data)

    return articles

if __name__ == "__main__":
    pdf_path = "Ποινικός-Κώδικας.pdf"
    output_json = "poinikos_kodikas.txt"

    articles = extract_penal_code_articles_fixed(pdf_path)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Εξήχθησαν {len(articles)} άρθρα και αποθηκεύτηκαν στο '{output_json}'")
