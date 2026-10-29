# Live Demo Script

## Preparation

1. Ensure verified documents are in `data/raw`.
2. Run preprocessing.
3. Generate embeddings.
4. Build ChromaDB.
5. Configure the LLM API in `.env`.
6. Run `python src/rag_chatbot.py`.

## Five realistic queries

1. "What are the requirements for the scholarship?"
2. "Who is eligible to apply?"
3. "When is the application period?"
4. "What benefits are provided?"
5. "How do I apply?"

## Out-of-scope query

"How do I repair a motorcycle?"

Expected behavior: PolyBot should flag the request as outside its scholarship
knowledge domain or state that it does not have enough verified information.

## Defense questions from the guide

- Why did you choose this distance metric/vector database?
- Walk through the query step by step.
- How do you reduce hallucinations?
- What would break if the collection grew 100x?
- What would you target with LoRA/QLoRA?
