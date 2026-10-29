# Prompt Engineering Document

## Prompt 1 — Grounded Scholarship Answer

**Purpose:** Force the model to answer from retrieved scholarship context.

**Key constraints:**
- Use only supplied context.
- Say that information is unavailable when context is insufficient.
- Do not invent deadlines, requirements, amounts, or eligibility.

**Hallucination prevention:** The explicit context-only rule and fallback
sentence reduce unsupported answers.

## Prompt 2 — Scope Guard

**Purpose:** Prevent off-topic responses.

Instruction:
Answer scholarship-information questions only. If the request is unrelated
to scholarships or cannot be answered from the knowledge base, politely flag
it as out of scope.

**Example:**
Question: "Who won the World Cup?"
Expected behavior: Refuse/flag as outside the scholarship knowledge domain.

## Prompt 3 — Decision Boundary

**Purpose:** Prevent the chatbot from making official decisions.

Instruction:
Explain eligibility criteria from the retrieved source, but never state that
a particular student is officially approved or rejected. Direct final
verification to the authorized scholarship office.

**Example:**
Question: "Am I officially qualified?"
Expected behavior: Explain the criteria if present, then state that the office
must make the final determination.
