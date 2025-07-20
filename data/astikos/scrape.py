import fitz  # PyMuPDF
import re

PDF_FILE = "Αστικός-Κώδικας.pdf"
TXT_OUTPUT = "astikos_kodikas_clean.txt"

# Χρήσιμο σημείο εκκίνησης του περιεχομένου
START_PATTERN = r"Αρθρο\s*:\s*1"

def extract_useful_text(pdf_path, txt_path, start_regex):
    doc = fitz.open(pdf_path)
    found_start = False
    useful_text = ""

    for page in doc:
        text = page.get_text()
        if not found_start:
            match = re.search(start_regex, text)
            if match:
                found_start = True
                text = text[match.start():]
                useful_text += text
        elif found_start:
            useful_text += text

    doc.close()

    # Φιλτράρισμα άχρηστων metadata
    cleaned_lines = []
    ignore_prefixes = (
        "Ημ/νία", "Ημ.Υπογραφής", "ΦΕΚ", "Τίτλος Αρθρου", "Περιγραφή όρου",
        "Λήμματα", "Σχόλια", "ΣΤΟΙΧΕΙΑ ΑΡΘΡΩΝ"
    )
    for line in useful_text.splitlines():
        line = line.strip()
        if (
            line and
            not any(line.startswith(prefix) for prefix in ignore_prefixes) and
            len(line) > 3
        ):
            cleaned_lines.append(line)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

    print(f"[✔] Το αρχείο αποθηκεύτηκε ως: {txt_path}")

if __name__ == "__main__":
    extract_useful_text(PDF_FILE, TXT_OUTPUT, START_PATTERN)
