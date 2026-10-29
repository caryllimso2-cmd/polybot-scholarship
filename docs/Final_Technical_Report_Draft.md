# Final Technical Report — Draft

## 1. Architecture

Data collection → preprocessing → embeddings → ChromaDB vector store →
retrieval → LangChain/Chat Completion model → terminal interface.

## 2. Data Pipeline

The pipeline reads text documents, cleans whitespace and control characters,
tokenizes text for inspection, generates sentence embeddings, and stores the
vectors for similarity search.

## 3. Prompt Design

Three prompt patterns are documented:
1. grounded scholarship answering
2. scope control
3. decision boundary / no official eligibility decisions

## 4. RAG Implementation

The CLI retrieves the most relevant scholarship documents from ChromaDB,
places them into the prompt context, and asks the language model to answer
only from that context.

## 5. Conversational Memory

The CLI stores recent human/assistant messages during a session. `/clear`
resets the session memory.

## 6. Deployment

The final target is a containerized application using Docker. Secrets such
as API keys are supplied through environment variables and are not committed
to source control.

## 7. Limitations

- Placeholder documents must be replaced with verified official records.
- Current CLI implementation depends on an OpenAI-compatible Chat Completion API.
- Knowledge-base freshness depends on the document update process.
- The system must not make official scholarship decisions.

## 8. Lessons Learned

The project demonstrates why preprocessing, embeddings, retrieval, prompt
constraints, and source grounding must work together. A chatbot can sound
confident even when information is missing, so the fallback and source-grounding
rules are important.
