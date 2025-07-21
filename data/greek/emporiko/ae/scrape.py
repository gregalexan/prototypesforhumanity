import fitz  # PyMuPDF
import re
import os

PDF_FILE = "AE_Corp.pdf"
OUTPUT_DIR = "./"
TXT_OUTPUT = os.path.join(OUTPUT_DIR, "ae_nomothesia_clean.txt")

START_PATTERN = r"Άρθρο\s+1"  # Ξεκινάμε από το πρώτο άρθρο

def extract_useful_text(pdf_path, txt_path, start_regex):
    doc = fitz.open(pdf_path)
    found_start = False
    useful_text = ""

    for page in doc:
        text = page.get_text()
        if not found_start:
            if re.search(start_regex, text):
                found_start = True
                text = re.split(start_regex, text, maxsplit=1)[-1]
                useful_text += "Άρθρο 1" + text
        elif found_start:
            useful_text += text

    doc.close()

    # Καθαρισμός περιττών γραμμών
    cleaned_lines = []
    for line in useful_text.splitlines():
        line = line.strip()
        if line and not line.lower().startswith("σελίδα") and len(line) > 3:
            cleaned_lines.append(line)

    os.makedirs(os.path.dirname(txt_path), exist_ok=True)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

    print(f"[✔] Το αρχείο αποθηκεύτηκε στο: {txt_path}")

if __name__ == "__main__":
    extract_useful_text(PDF_FILE, TXT_OUTPUT, START_PATTERN)
