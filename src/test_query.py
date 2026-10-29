from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "chroma_db"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=str(DB))
collection = client.get_collection("polybot_scholarships")

query = input("Query: ").strip()
qvec = model.encode([query], normalize_embeddings=True).tolist()

result = collection.query(
    query_embeddings=qvec,
    n_results=5
)

print("\nTOP RESULTS")
print("=" * 60)

for i, (doc, meta, distance) in enumerate(
    zip(
        result["documents"][0],
        result["metadatas"][0],
        result["distances"][0]
    ),
    start=1
):
    print(f"\n{i}. {meta['title']}")
    print(f"Distance: {distance:.4f}")
    print(doc[:500].replace("\n", " "))
