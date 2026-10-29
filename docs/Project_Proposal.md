# Project Proposal

## Title
**PolyBot: Scholarship Information Chatbot**

## Problem Statement
Students often need scholarship information such as eligibility, requirements,
benefits, deadlines, and application procedures. Information may be spread
across multiple documents or announcements. PolyBot proposes a grounded
generative-AI assistant that retrieves relevant scholarship documents before
generating an answer.

## Target Users
- Students seeking scholarship information
- Scholarship coordinators/authorized personnel
- Academic support personnel

## Theme
Document/Knowledge-Base Q&A Assistant, aligned with the guide's suggested
generative-AI theme.

## Dataset Sources
The development repository contains 24 simulated/template text documents.
These demonstrate the required 20–30 document/page scope. For real deployment,
they must be replaced or supplemented with verified scholarship-office
documents and official announcements.

## Success Criteria
1. At least 20–30 relevant text documents are ingested.
2. Text cleaning and tokenization are demonstrated with before/after evidence.
3. Embeddings are generated successfully.
4. Vector similarity search retrieves relevant scholarship documents.
5. RAG responses remain grounded in retrieved context.
6. At least one out-of-scope query is correctly flagged.
7. Multi-turn conversational memory works in the CLI.
8. The application can be packaged in Docker for the final checkpoint.

## Team Division
- Carylflor Osmil — leadership, integration, documentation
- Angelo Batausa — data collection and preprocessing
- Ryan Rodriguez — embeddings, ChromaDB, retrieval and RAG
- Gevanny Autida — interface, testing and deployment support
