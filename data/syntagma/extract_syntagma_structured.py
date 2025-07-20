import re
import pdfplumber
 
def extract_syntagma_plaintext(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i >= 19:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
 
    # Καθαρισμοί
    text = re.sub(r"(?<=\S)-\n(?=\S)", "", text)
    text = re.sub(r"\n+", "\n", text)
 
    # Διάσπαση σε άρθρα
    pattern = r"(Άρθρ[οoOΟ]\s*\d+[Α-Ω]?)"
    splits = re.split(pattern, text)
 
    output_lines = []
    for i in range(1, len(splits), 2):
        article_number = splits[i].strip().replace("Άρθρο", "").replace("Άρθρo", "").strip()
        content_block = splits[i + 1].strip()
 
        output_lines.append(f"Άρθρο {article_number}\n{content_block}\n\n")
 
    return "".join(output_lines)
 
if __name__ == "__main__":
    pdf_path = "syntagma1_1.pdf"
    output_txt = "syntagma_plaintext.txt"
 
    plain_text = extract_syntagma_plaintext(pdf_path)
 
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(plain_text)
 
    print(f"✅ Αποθηκεύτηκε ως απλό txt στο '{output_txt}'")
 
 