import fitz  # PyMuPDF
import re

PDF_FILE = "Kodikas_Dioikitikis_Diadikasias.pdf"
TXT_OUTPUT = "kodikas_dioikitikis_diadikasias_clean.txt"

# Πιο γενική regex που εντοπίζει άρθρα
START_PATTERN = r"(Αρθρο\s*:?\s*1|Άρθρο\s*:?\s*1|ΑΡΘΡΟ\s+1|ΑΡΘΡΟ\s+ΠΡΩΤΟ)"

def extract_useful_text(pdf_path, txt_path, start_regex):
    doc = fitz.open(pdf_path)
    found_start = False
    useful_text = ""

    for page in doc:
        text = page.get_text()
        if not found_start:
            match = re.search(start_regex, text, flags=re.IGNORECASE)
            if match:
                found_start = True
                text = text[match.start():]
                useful_text += text
        elif found_start:
            useful_text += text

    doc.close()

    # Καθαρισμός γραμμών και headers
    cleaned_lines = []
    for line in useful_text.splitlines():
        line = line.strip()
        if (
            line and
            not line.lower().startswith("σελίδα") and
            not line.startswith("ΦΕΚ") and
            not re.match(r"^\s*Ημ.*?:", line) and
            len(line) > 3
        ):
            cleaned_lines.append(line)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

    print(f"[✔] Το αρχείο αποθηκεύτηκε ως: {txt_path}")

if __name__ == "__main__":
    extract_useful_text(PDF_FILE, TXT_OUTPUT, START_PATTERN)
