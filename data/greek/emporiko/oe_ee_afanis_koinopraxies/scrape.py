import fitz  # PyMuPDF
import re

PDF_FILE = "OE_EE_Corps.pdf"
TXT_OUTPUT = "oe_ee_clean.txt"

START_PATTERN = r"Άρθρο\s+249"

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
                useful_text += "Άρθρο 249" + text
        elif found_start:
            useful_text += text

    doc.close()

    # Καθαρισμός περιττών γραμμών
    cleaned_lines = []
    for line in useful_text.splitlines():
        line = line.strip()
        if line and not line.lower().startswith("σελίδα") and len(line) > 3:
            cleaned_lines.append(line)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

    print(f"[✔] Το αρχείο αποθηκεύτηκε ως: {txt_path}")

if __name__ == "__main__":
    extract_useful_text(PDF_FILE, TXT_OUTPUT, START_PATTERN)
