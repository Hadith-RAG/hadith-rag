"""
Fetch 100 hadiths from the local sunnah.com API and write to data.py.

Prerequisites:
    cd api && docker compose up -d

Usage:
    python fetch_data.py
"""

import json
import requests


API_URL = "http://localhost:5000/v1/hadiths"
HEADERS = {"x-aws-secret": "secret"}


def fetch_and_save():
    print("Fetching 100 hadiths from API...")

    resp = requests.get(
        API_URL,
        headers=HEADERS,
        params={"collection": "bukhari", "limit": 100, "page": 1},
        timeout=30,
    )
    resp.raise_for_status()

    hadiths_raw = resp.json().get("data", [])
    print(f"  Got {len(hadiths_raw)} hadiths from API")

    # Extract English text from each hadith
    entries = []
    for h in hadiths_raw:
        # Find the English body
        en = next((x for x in h.get("hadith", []) if x["lang"] == "en"), None)
        if not en or not en.get("body"):
            continue

        entries.append(
            {
                "id": f"bukhari_{h['hadithNumber']}",
                "text": en["body"].strip(),
                "book": "bukhari",
                "number": h["hadithNumber"],
            }
        )

    # Write data.py
    with open("data.py", "w", encoding="utf-8") as f:
        f.write("hadiths = [\n")
        for i, entry in enumerate(entries):
            f.write("    {\n")
            f.write(f'        "id": {json.dumps(entry["id"])},\n')
            f.write(f'        "text": {json.dumps(entry["text"])},\n')
            f.write(f'        "book": {json.dumps(entry["book"])},\n')
            f.write(f'        "number": {json.dumps(entry["number"])}\n')
            f.write("    }")
            if i < len(entries) - 1:
                f.write(",")
            f.write("\n")
        f.write("]\n")

    print(f"Done! data.py now contains {len(entries)} hadiths.")


if __name__ == "__main__":
    fetch_and_save()
