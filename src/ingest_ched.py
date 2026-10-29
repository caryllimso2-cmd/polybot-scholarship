from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# Locate project root and ChromaDB path
ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "chroma_db"

# Initialize model and database client
print("Initializing embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=str(DB))

# Fetch your existing collection
collection = client.get_collection("polybot_scholarships")

# CHED Merit Scholarship Knowledge Text
ched_document = """
Title: CHED Merit Scholarship Program (CMSP) Guidelines
Overview: The CHED Merit Scholarship Program provides financial assistance to academically talented and deserving Filipino students pursuing undergraduate degrees in priority programs.

Eligibility Requirements:
- Must be a Filipino citizen.
- Must be a graduating senior high school student or high school graduate with a minimum General Weighted Average (GWA) of 93% or its equivalent.
- Combined annual gross income of parents or legal guardian must not exceed PHP 500,000.
- Must secure admission in State Universities and Colleges (SUCs), Local Universities and Colleges (LUCs) with Institutional Recognition/COPC, or CHED-recognized Private HEIs.

Documentary Requirements:
- Accomplished Online Application Form / Annex A
- Birth Certificate (PSA or NSO copy)
- Certified true copy of Grade 12 School Form 9 (SF9) / Form 138 (High School Report Card)
- Proof of income (any one applicable): Latest Income Tax Return (ITR), BIR Certificate of Tax Exemption/Non-Filer, DSWD Certificate of Indigence/Case Study Report, or latest contract/proof of income for OFWs and seafarers.
- Special group documents if applicable (e.g., PWD ID, Solo Parent ID, Indigenous Peoples Certification from NCIP).

Coverage and Financial Benefits:
- Covers tuition and other school fees (TOSF) for private HEI slots or free tuition under SUCs/LUCs.
- Provides a regular stipend released directly to scholars or through Higher Education Institutions.
- Includes a book and connectivity allowance per semester until the completion of the degree program.

Application Process:
- Prepare and scan clear digital copies of all required documents.
- Submit applications online through the official CHED Regional Office (CHEDRO) portal or links provided by respective regional offices based on your point of origin.
- Reference Link: https://legacy.ched.gov.ph/merit-scholarship/
"""

# Generate vector embedding
print("Embedding CHED scholarship document...")
vector = model.encode([ched_document], normalize_embeddings=True).tolist()

# Add to ChromaDB collection
collection.upsert(
    documents=[ched_document],
    metadatas=[{"title": "CHED Merit Scholarship Program Guidelines"}],
    ids=["ched_merit_scholarship_01"]
)

print("Successfully added CHED Merit Scholarship data to PolyBot's ChromaDB database!")