"""
Generate data.py with the first 100 hadiths from Sahih al-Bukhari.

Reads from: hadith-json/db/by_book/the_9_books/bukhari.json
Writes to:  hadith-rag/data.py
"""

import json
from pathlib import Path

HADITH_COUNT = 100

# Paths
script_dir = Path(__file__).resolve().parent
json_path = script_dir.parent / "hadith-json" / "db" / "by_book" / "the_9_books" / "bukhari.json"
output_path = script_dir / "data.py"

# Load source JSON
print(f"Reading {json_path} ...")
with open(json_path, "r", encoding="utf-8") as f:
    book = json.load(f)

book_title = book["metadata"]["english"]["title"]  # "Sahih al-Bukhari"
all_hadiths = book["hadiths"]
print(f"Total hadiths in {book_title}: {len(all_hadiths)}")

# Extract first 100
selected = all_hadiths[:HADITH_COUNT]

# Build entries matching the data.py schema
entries = []
for h in selected:
    narrator = h["english"]["narrator"].strip()
    text = h["english"]["text"].strip()
    # Combine narrator + text for full English context
    full_text = f"{narrator} {text}" if narrator else text
    entries.append({
        "id": f"bukhari_{h['idInBook']}",
        "text": full_text,
        "book": book_title,
        "number": h["idInBook"],
    })

# Write data.py
print(f"Writing {len(entries)} hadiths to {output_path} ...")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("hadiths = [\n")
    for i, entry in enumerate(entries):
        # Use json.dumps for safe string escaping
        f.write("    {\n")
        f.write(f'        "id": {json.dumps(entry["id"])},\n')
        f.write(f'        "text": {json.dumps(entry["text"])},\n')
        f.write(f'        "book": {json.dumps(entry["book"])},\n')
        f.write(f'        "number": {entry["number"]}\n')
        f.write("    }")
        if i < len(entries) - 1:
            f.write(",")
        f.write("\n")
    f.write("]\n")

print(f"Done! {output_path.name} now contains {len(entries)} hadiths from {book_title}.")
