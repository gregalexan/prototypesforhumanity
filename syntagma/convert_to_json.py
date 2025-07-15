import json

def txt_to_json(txt_path, json_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    articles = []
    current_article = {}
    content_lines = []

    for line in lines:
        line = line.strip()

        if line.startswith("Άρθρο "):
            # Αν ήδη είχαμε άρθρο, το αποθηκεύουμε
            if current_article:
                current_article["content"] = "\n".join(content_lines).strip()
                articles.append(current_article)
                content_lines = []

            number = line.replace("Άρθρο", "").strip()
            current_article = {
                "article_number": number,
                "title": f"Άρθρο {number}",
                "country": "Greece",
                "law_type": "Σύνταγμα",
                "content": ""  # θα προστεθεί μετά
            }

        elif line.startswith("=" * 10):
            # Τέλος άρθρου, αποθήκευση
            if current_article:
                current_article["content"] = "\n".join(content_lines).strip()
                articles.append(current_article)
                current_article = {}
                content_lines = []
        else:
            content_lines.append(line)

    # Μην ξεχάσεις το τελευταίο άρθρο
    if current_article and content_lines:
        current_article["content"] = "\n".join(content_lines).strip()
        articles.append(current_article)

    # Αποθήκευση JSON
    with open(json_path, "w", encoding="utf-8") as out:
        json.dump(articles, out, ensure_ascii=False, indent=2)

    print(f"✅ Μετατροπή ολοκληρώθηκε: {len(articles)} άρθρα")

# Χρήση
txt_to_json("syntagma_final.txt", "syntagma_articles.json")
