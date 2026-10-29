from pathlib import Path
import json
import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "processed_documents.json"
DB = ROOT / "chroma_db"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

records = json.loads(INPUT.read_text(encoding="utf-8"))
model = SentenceTransformer(MODEL_NAME)

client = chromadb.PersistentClient(path=str(DB))

collection = client.get_or_create_collection(
    name="polybot_scholarships",
    metadata={"hnsw:space": "cosine"}
)

ids = [r["id"] for r in records]
documents = [r["cleaned_text"] for r in records]
metadatas = [
    {
        "filename": r["filename"],
        "source": r["source"],
        "title": r["filename"].replace("_", " ").replace(".txt", "")
    }
    for r in records
]

embeddings = model.encode(
    documents,
    normalize_embeddings=True
).tolist()

collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)

print(f"Indexed {collection.count()} documents in ChromaDB.")
