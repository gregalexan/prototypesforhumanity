from pathlib import Path
import re

# Αρχεία εισόδου
core_path = Path("core_instruments_list.txt")
universal_path = Path("universal_instruments_list.txt")
output_path = Path("instruments_list.txt")

def load_entries(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().strip().splitlines()

    # Χωρίζουμε ανά δύο γραμμές: τίτλος και URL
    entries = []
    for i in range(0, len(lines), 2):
        if i+1 < len(lines):
            title = lines[i].strip()
            url = lines[i+1].strip()
            entries.append((title, url))
    return entries

def main():
    core_entries = load_entries(core_path)
    universal_entries = load_entries(universal_path)

    combined = core_entries + universal_entries

    # Αφαίρεση διπλότυπων βάσει URL
    seen_urls = set()
    unique_entries = []
    for title, url in combined:
        if url not in seen_urls:
            seen_urls.add(url)
            unique_entries.append((title, url))

    # Αποθήκευση σε νέο αρχείο
    with open(output_path, "w", encoding="utf-8") as f:
        for title, url in unique_entries:
            f.write(f"{title}\n{url}\n\n")

    print(f"✅ Merged {len(unique_entries)} unique instruments into {output_path.name}")

if __name__ == "__main__":
    main()
