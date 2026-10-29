# LangChain vs LlamaIndex — Framework Comparison Note

## LangChain

LangChain provides composable components for prompts, models, retrievers,
message history, and chains. In PolyBot it is used for the LLM interface
and conversation message handling, while ChromaDB performs vector storage
and retrieval.

## LlamaIndex

LlamaIndex is strongly oriented toward ingesting, indexing, and querying
document collections. It provides document/node abstractions and retrieval
components that can be useful for a knowledge-base application.

## Choice

PolyBot uses **LangChain** for the RAG orchestration layer in the CLI
prototype and **ChromaDB** as the vector database. The choice keeps the
application modular: preprocessing and embeddings are separate scripts,
Chroma handles similarity search, and LangChain handles prompt/model
orchestration and conversational messages.

The project does not claim to use LlamaIndex unless it is actually added.
