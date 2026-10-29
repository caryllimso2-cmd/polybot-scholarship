from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

def clean_text(text: str) -> str:
    text = text.replace("\ufeff", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[^\S\r\n]+", " ", text)
    return text.strip()

def tokenize(text: str):
    return re.findall(r"\b[\w'-]+\b", text.lower())

records = []

for path in sorted(RAW.glob("*.txt")):
    if path.name == "README.md":
        continue
    raw = path.read_text(encoding="utf-8")
    cleaned = clean_text(raw)
    tokens = tokenize(cleaned)

    records.append({
        "id": path.stem,
        "filename": path.name,
        "raw_text": raw,
        "cleaned_text": cleaned,
        "tokens": tokens,
        "token_count": len(tokens),
        "source": "SIMULATED/TEMPLATE - replace with official source"
    })

(OUT / "processed_documents.json").write_text(
    json.dumps(records, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"Processed {len(records)} documents.")
print("\nBefore/after example:")
if records:
    print("\n--- BEFORE ---")
    print(records[0]["raw_text"][:700])
    print("\n--- AFTER ---")
    print(records[0]["cleaned_text"][:700])
    print(f"\nTokens: {records[0]['token_count']}")
