import fitz  # PyMuPDF
import re

PDF_FILE = "Κώδικας-Μετανάστευσης.pdf"
TXT_OUTPUT = "metanasteftikos_kodikas_clean.txt"

# Εντολή έναρξης περιεχομένου
START_TEXT = "ΜΕΡΟΣ Α’"

# Αγνοούμε headers/footers
IGNORE_LINES = (
    "ΕΦΗΜΕΡΙΔΑ", "ΤΗΣ ΚΥΒΕΡΝΗΣΕΩΣ", "ΤΗΣ ΕΛΛΗΝΙΚΗΣ ΔΗΜΟΚΡΑΤΙΑΣ",
    "Τεύχος", "Αρ.", "Φύλλου", "Σελίδα", "01.04.2023"
)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    start_found = False

    for page_num, page in enumerate(doc):
        blocks = page.get_text("blocks")  # get list of text blocks (x0, y0, x1, y1, "text", block_no, block_type)
        blocks.sort(key=lambda b: (b[1], b[0]))  # sort by vertical (y0), then horizontal (x0)

        page_text = ""
        for b in blocks:
            txt = b[4].strip()
            if txt:
                page_text += txt + "\n"

        if not start_found:
            if START_TEXT in page_text:
                start_found = True
                idx = page_text.index(START_TEXT)
                full_text += page_text[idx:] + "\n"
        elif start_found:
            full_text += page_text + "\n"

    doc.close()
    return full_text

def clean_text(raw_text):
    lines = raw_text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(line.startswith(p) for p in IGNORE_LINES):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)

def save_to_file(text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[✔] Αποθηκεύτηκε: {path}")

if __name__ == "__main__":
    raw = extract_text_from_pdf(PDF_FILE)
    cleaned = clean_text(raw)
    save_to_file(cleaned, TXT_OUTPUT)
