from pathlib import Path
import os
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DB = ROOT / "chroma_db"
EMBED_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL = os.getenv("LLM_MODEL")

if not API_KEY or not BASE_URL or not MODEL:
    print("Missing LLM_API_KEY, LLM_BASE_URL, or LLM_MODEL in .env")
    print("The vector retrieval demo still works with src/test_query.py.")
    raise SystemExit(1)

embedder = SentenceTransformer(EMBED_MODEL)
client = chromadb.PersistentClient(path=str(DB))
collection = client.get_collection("polybot_scholarships")

llm = ChatOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    model=MODEL,
    temperature=0
)

history = []

SYSTEM_PROMPT = """You are PolyBot, a scholarship information assistant.

RULES:
1. Answer ONLY from the supplied CONTEXT.
2. If the context does not contain enough information, say:
   "I don't have enough verified information in my knowledge base."
3. Never invent eligibility rules, amounts, deadlines, contacts, or requirements.
4. Do not make final scholarship decisions.
5. Treat official scholarship-office information as authoritative.
6. Keep answers concise and student-friendly.
7. When useful, mention the source document title.
"""

def retrieve(question, k=4):
    vector = embedder.encode(
        [question],
        normalize_embeddings=True
    ).tolist()

    return collection.query(
        query_embeddings=vector,
        n_results=k
    )

def build_context(result):
    blocks = []
    for doc, meta in zip(
        result["documents"][0],
        result["metadatas"][0]
    ):
        blocks.append(
            f"SOURCE: {meta['title']}\n{doc}"
        )
    return "\n\n---\n\n".join(blocks)

def ask(question):
    result = retrieve(question)
    context = build_context(result)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *history[-6:],
        HumanMessage(
            content=(
                f"CONTEXT:\n{context}\n\n"
                f"QUESTION:\n{question}"
            )
        )
    ]

    response = llm.invoke(messages)
    answer = response.content

    history.append(HumanMessage(content=question))
    history.append(AIMessage(content=answer))

    return answer

print("\n" + "=" * 64)
print("POLYBOT — SCHOLARSHIP INFORMATION CHATBOT")
print("RAG CLI • Type /exit to quit • Type /clear to clear memory")
print("=" * 64)

while True:
    question = input("\nYou: ").strip()

    if not question:
        continue

    if question.lower() == "/exit":
        print("PolyBot: Goodbye!")
        break

    if question.lower() == "/clear":
        history.clear()
        print("PolyBot: Conversation memory cleared.")
        continue

    try:
        print("\nPolyBot:")
        print(ask(question))
    except Exception as exc:
        print(f"Error: {exc}")
