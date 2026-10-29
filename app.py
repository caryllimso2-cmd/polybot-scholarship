import os
from pathlib import Path
import streamlit as st
import chromadb
import chromadb.utils.embedding_functions as ef
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PolyBot — Scholarship Information Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENVIRONMENT & CONFIGURATION ---
ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# Priority: Streamlit secrets (for cloud deployment) > Environment variables > Local .env
def get_secret(key: str, default: str = "") -> str:
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)

DEFAULT_API_KEY = get_secret("LLM_API_KEY") or get_secret("GROQ_API_KEY")
DEFAULT_BASE_URL = get_secret("LLM_BASE_URL", "https://api.groq.com/openai/v1")
DEFAULT_MODEL = get_secret("LLM_MODEL", "openai/gpt-oss-20b")
CHROMA_DIR = ROOT / "chroma_db"

SYSTEM_PROMPT = """You are PolyBot, an official scholarship guidance assistant.
Your goal is to assist students with accurate, grounded information about the CHED Merit Scholarship Program (CMSP) and college scholarship policies.

STRICT OPERATIONAL RULES:
1. Answer ONLY using the facts provided in the CONTEXT below.
2. If the context does not contain enough information to answer accurately, explicitly reply:
   "I do not have enough verified information in my knowledge base to answer this question. Please consult the official CHED Regional Office (CHEDRO) or the campus scholarship office."
3. Do NOT speculate, extrapolate, or fabricate any deadlines, income thresholds, grade requirements, or monetary amounts.
4. Always cite the relevant document source title when providing answers.
5. Keep your tone encouraging, professional, and student-friendly.
"""

# --- DATABASE & EMBEDDING INITIALIZATION ---
@st.cache_resource(show_spinner=False)
def get_vector_store():
    """Initializes ChromaDB with ONNX-powered all-MiniLM-L6-v2 embeddings."""
    embedding_fn = ef.DefaultEmbeddingFunction()
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(
        name="polybot_scholarships",
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    # Auto-ingest if collection is empty (e.g. freshly deployed on Streamlit Community Cloud)
    if collection.count() == 0:
        docs_to_index = []
        metas_to_index = []
        ids_to_index = []
        
        # Ingest CHED document if available
        ched_file = ROOT / "data" / "raw" / "00_ched_merit_scholarship.txt"
        if not ched_file.exists():
            ched_file = ROOT / "data" / "ched_merit_scholarship.txt"
        
        if ched_file.exists():
            content = ched_file.read_text(encoding="utf-8")
            docs_to_index.append(content)
            metas_to_index.append({
                "title": "CHED Merit Scholarship Program Guidelines",
                "filename": ched_file.name,
                "source": "Commission on Higher Education (CHED) Official Guidelines"
            })
            ids_to_index.append("ched_merit_scholarship_01")
        
        # Ingest raw text files
        raw_dir = ROOT / "data" / "raw"
        if raw_dir.exists():
            for txt_path in sorted(raw_dir.glob("*.txt")):
                if txt_path.name == ched_file.name:
                    continue
                content = txt_path.read_text(encoding="utf-8")
                title = txt_path.stem.replace("_", " ").title()
                docs_to_index.append(content)
                metas_to_index.append({
                    "title": title,
                    "filename": txt_path.name,
                    "source": "Institutional Scholarship Policy Template"
                })
                ids_to_index.append(txt_path.stem)
                
        if docs_to_index:
            collection.add(
                documents=docs_to_index,
                metadatas=metas_to_index,
                ids=ids_to_index
            )
            
    return collection

def retrieve_context(collection, query: str, k: int = 3):
    """Retrieves top-k context passages from ChromaDB."""
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    
    documents = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    distances = results["distances"][0] if "distances" in results and results["distances"] else []
    
    formatted_context_blocks = []
    citations = []
    
    for i, (doc, meta) in enumerate(zip(documents, metadatas)):
        title = meta.get("title", f"Document {i+1}")
        source = meta.get("source", "Knowledge Base")
        dist = distances[i] if i < len(distances) else None
        
        formatted_context_blocks.append(f"### SOURCE [{i+1}]: {title} ({source})\n{doc}")
        citations.append({
            "index": i + 1,
            "title": title,
            "source": source,
            "distance": dist,
            "snippet": doc[:300] + "..." if len(doc) > 300 else doc
        })
        
    joined_context = "\n\n---\n\n".join(formatted_context_blocks)
    return joined_context, citations

# --- SIDEBAR & SETTINGS ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/graduation-cap.png", width=110)
    st.title("PolyBot Settings")
    st.caption("Gen AI Semester Project • RAG Architecture")
    
    st.markdown("---")
    st.subheader("⚙️ LLM Configuration")
    user_api_key = st.text_input(
        "Groq / OpenAI API Key",
        value=DEFAULT_API_KEY,
        type="password",
        help="Leave empty to use the system configured key, or enter your personal key."
    )
    selected_model = st.selectbox(
        "Model",
        options=["openai/gpt-oss-20b", "openai/gpt-oss-120b", "qwen/qwen3.8-27b", "llama3-8b-8192", "mixtral-8x7b-32768"],
        index=0 if DEFAULT_MODEL == "openai/gpt-oss-20b" else 0
    )
    base_url = st.text_input("Base URL", value=DEFAULT_BASE_URL)
    
    st.markdown("---")
    st.subheader("📊 System Specs")
    st.markdown(
        """
        - **Pipeline**: Retrieval-Augmented Generation (RAG)
        - **Embedding Model**: `all-MiniLM-L6-v2` (ONNX Runtime, 384-dim)
        - **Vector Store**: ChromaDB (Cosine similarity metric)
        - **LLM Engine**: Groq Fast Inference API
        - **Framework**: LangChain + Streamlit
        """
    )
    
    st.markdown("---")
    st.subheader("⚠️ Free-Tier Quota Notice")
    st.info(
        "**Usage Limit:** This deployment runs on a free-tier Groq API quota (~30 requests/min). "
        "If rate limits occur during evaluation, please wait 30 seconds before submitting another prompt."
    )
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🎓 PolyBot: Scholarship Information Assistant")
st.markdown(
    "Welcome! Ask questions about **CHED Merit Scholarship Program (CMSP)** eligibility, "
    "documentary requirements, financial benefits, and college scholarship policies. "
    "All responses are **grounded in verified documents** with traceable citations."
)

# Suggested Sample Questions
st.markdown("##### 💡 Try asking:")
sample_col1, sample_col2, sample_col3, sample_col4 = st.columns(4)

prompt_to_send = None
if sample_col1.button("📋 CHED Eligibility", use_container_width=True):
    prompt_to_send = "What are the eligibility requirements for the CHED Merit Scholarship Program?"
if sample_col2.button("💵 Income Limit", use_container_width=True):
    prompt_to_send = "What is the maximum family gross income allowed to qualify for CHED?"
if sample_col3.button("📑 Required Docs", use_container_width=True):
    prompt_to_send = "What documentary requirements must I submit for the scholarship application?"
if sample_col4.button("🚀 Out-of-Scope Test", use_container_width=True):
    prompt_to_send = "How do I apply for a NASA astronaut pilot spaceflight grant?"

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am PolyBot, your scholarship information assistant. How can I help you with scholarship requirements or application procedures today?",
            "citations": []
        }
    ]

# Display Existing Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander("📚 Retrieved Sources & Grounding Passages", expanded=False):
                for cit in msg["citations"]:
                    st.markdown(f"**[{cit['index']}] {cit['title']}** — *{cit['source']}*")
                    if cit.get("distance") is not None:
                        st.caption(f"Cosine Distance: {cit['distance']:.4f}")
                    st.code(cit["snippet"], language="text")

# Chat Input & User Prompt Handling
user_input = st.chat_input("Ask a question about scholarships...")
if prompt_to_send:
    user_input = prompt_to_send

if user_input:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Validate API Key
    effective_key = user_api_key or DEFAULT_API_KEY
    if not effective_key:
        with st.chat_message("assistant"):
            st.error("⚠️ Missing API Key! Please enter your Groq API key in the sidebar or set `LLM_API_KEY` in environment variables.")
        st.stop()

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Retrieving relevant scholarship documents..."):
            try:
                collection = get_vector_store()
                context, citations = retrieve_context(collection, user_input, k=3)
                
                # Setup LangChain LLM Client
                llm = ChatOpenAI(
                    api_key=effective_key,
                    base_url=base_url,
                    model=selected_model,
                    temperature=0
                )
                
                # Build Message Payload with Conversation History (last 4 turns)
                history_payload = []
                for prev in st.session_state.messages[-5:-1]:
                    if prev["role"] == "user":
                        history_payload.append(HumanMessage(content=prev["content"]))
                    elif prev["role"] == "assistant":
                        history_payload.append(AIMessage(content=prev["content"]))

                rag_prompt = (
                    f"CONTEXT FROM KNOWLEDGE BASE:\n"
                    f"{context}\n\n"
                    f"STUDENT QUESTION:\n"
                    f"{user_input}"
                )
                
                messages = [
                    SystemMessage(content=SYSTEM_PROMPT),
                    *history_payload,
                    HumanMessage(content=rag_prompt)
                ]
                
                response = llm.invoke(messages)
                answer_text = response.content
                
                st.markdown(answer_text)
                
                if citations:
                    with st.expander("📚 Retrieved Sources & Grounding Passages", expanded=False):
                        for cit in citations:
                            st.markdown(f"**[{cit['index']}] {cit['title']}** — *{cit['source']}*")
                            if cit.get("distance") is not None:
                                st.caption(f"Cosine Distance: {cit['distance']:.4f}")
                            st.code(cit["snippet"], language="text")
                
                # Record in Session State
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer_text,
                    "citations": citations
                })

            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
