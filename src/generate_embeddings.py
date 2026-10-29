from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "processed_documents.json"
OUT = ROOT / "data" / "processed" / "embeddings.npz"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

records = json.loads(INPUT.read_text(encoding="utf-8"))
texts = [r["cleaned_text"] for r in records]

print(f"Loading embedding model: {MODEL_NAME}")
model = SentenceTransformer(MODEL_NAME)

vectors = model.encode(
    texts,
    normalize_embeddings=True,
    show_progress_bar=True
)

np.savez_compressed(
    OUT,
    embeddings=np.asarray(vectors, dtype=np.float32),
    ids=np.array([r["id"] for r in records])
)

print(f"Generated {len(vectors)} embeddings.")
print(f"Embedding dimension: {vectors.shape[1]}")
print(f"Saved to: {OUT}")
