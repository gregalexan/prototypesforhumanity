import fitz  # PyMuPDF
import re

# Ορισμός paths
PDF_FILE = "kodikas_dikigoron.pdf"
TXT_OUTPUT = "kodikas_dikigoron_clean.txt"

# Ορισμός λέξης-κλειδί για την έναρξη των χρήσιμων δεδομένων
START_PATTERN = r"ΚΩΔΙΚΑΣ ΔΙΚΗΓΟΡΩΝ\s+ΚΕΦΑΛΑΙΟ Α’\s+–\s+Γενικό Μέρος"

def extract_useful_text(pdf_path, txt_path, start_regex):
    doc = fitz.open(pdf_path)
    found_start = False
    useful_text = ""

    for page in doc:
        text = page.get_text()
        if not found_start:
            if re.search(start_regex, text):
                found_start = True
                # Κόψε το κείμενο από το σημείο έναρξης και μετά
                text = re.split(start_regex, text, maxsplit=1)[-1]
                useful_text += "ΚΩΔΙΚΑΣ ΔΙΚΗΓΟΡΩΝ\nΚΕΦΑΛΑΙΟ Α’ – Γενικό Μέρος\n" + text
        elif found_start:
            useful_text += text

    doc.close()

    # Αφαίρεση γραμμών με πολλές κενές ή άσχετες λέξεις (προαιρετική καθαριότητα)
    cleaned_lines = []
    for line in useful_text.splitlines():
        line = line.strip()
        if line and not line.startswith("Σελίδα") and len(line) > 3:
            cleaned_lines.append(line)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

    print(f"[✔] Το καθαρισμένο αρχείο σώθηκε ως: {txt_path}")

if __name__ == "__main__":
    extract_useful_text(PDF_FILE, TXT_OUTPUT, START_PATTERN)
