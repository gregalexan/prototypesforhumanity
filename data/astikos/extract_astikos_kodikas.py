import re
import json
from PyPDF2 import PdfReader

def extract_articles_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = "\n".join([page.extract_text() for page in reader.pages])

    # Ανίχνευση άρθρων με τίτλο: "Αρθρο: <αριθμός>"
    pattern = r"(Αρθρο:\s*\d+.*?)\n(?=Αρθρο:|\Z)"
    matches = re.findall(pattern, full_text, re.DOTALL)

    articles = []
    for match in matches:
        # Ανίχνευση αριθμού άρθρου
        article_num_match = re.search(r"Αρθρο:\s*(\d+)", match)
        article_num = article_num_match.group(1) if article_num_match else "Χωρίς αριθμό"

        # Ανίχνευση τίτλου αν υπάρχει
        title_match = re.search(r"Τίτλος Αρθρου\s*(.*?)\n", match)
        title = title_match.group(1).strip() if title_match else ""

        # Απομόνωση του κυρίως κειμένου του άρθρου
        content_match = re.search(r"Κείμενο Αρθρου\s*(.*)", match, re.DOTALL)
        content = content_match.group(1).strip() if content_match else match.strip()

        articles.append({
            "title": "Αστικός Κώδικας",
            "article": f"Άρθρο {article_num}",
            "headline": title,
            "content": content
        })

    return articles

if __name__ == "__main__":
    pdf_path = "Αστικός-Κώδικας.pdf"
    output_json = "astikos_kodikas.json"

    articles = extract_articles_from_pdf(pdf_path)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Εξήχθησαν {len(articles)} άρθρα και αποθηκεύτηκαν στο '{output_json}'")
