# PolyBot — Demo Video Recording Script 🎬
**Target Length**: 5 to 8 Minutes  
**Rubric Points**: 20 Points (Criterion 4)

---

## 📋 Pre-Recording Checklist
- [ ] Deploy the web app to **Streamlit Community Cloud** (so the URL in your browser bar is public, e.g. `https://polybot-scholarship.streamlit.app`).
- [ ] Open the app in your browser before starting the recording.
- [ ] Ensure your microphone is clear.
- [ ] Have the 3 sample questions ready to copy/paste or click using the sample buttons.

---

## ⏱️ Video Outline & Timestamps

| Section | Target Time | Description |
| :--- | :--- | :--- |
| **Part 1: Problem & Knowledge Source** | 0:00 – 1:15 | Intro, team names, problem being solved, and CHED knowledge base. |
| **Part 2: System Architecture** | 1:15 – 2:30 | Embedding model, ChromaDB vector store, Groq LLM, LangChain. |
| **Part 3: Live Walkthrough of Deployed App** | 2:30 – 3:45 | Overview of the UI, sidebar settings, quota badge, no-login access. |
| **Part 4: 3 Sample Questions (Live Testing)** | 3:45 – 6:00 | 2 grounded scholarship queries + 1 out-of-scope query. |
| **Part 5: Limitations & Future Improvements** | 6:00 – 7:00 | PDF parsing, multi-lingual support, student portal API integration. |

---

## 🎙️ Word-for-Word Script

### Part 1: Problem & Knowledge Source (0:00 – 1:15)
> *"Hello everyone and greetings to our instructor! Today, our team is proud to present **PolyBot: Scholarship Information Assistant**, our semester capstone project for Generative AI.*
>
> *Our team members are Carylflor Osmil, Angelo Batausa, Ryan Rodriguez, and Gevanny Autida.*
>
> *Every semester, college applicants and undergraduate students face significant hurdles navigating complex scholarship guidelines. Important rules regarding grade point averages, income ceilings, and documentary requirements are often buried in dense memos. Many students miss opportunities simply because the guidelines are difficult to decipher.*
>
> *To solve this, we created PolyBot. Our primary knowledge base is the official **CHED Merit Scholarship Program (CMSP)** guidelines published by the Commission on Higher Education, supplemented by institutional scholarship policy records. We ingested and processed these documents to ensure all answers provided to students are 100% verified and traceable to official sources."*

---

### Part 2: System Architecture (1:15 – 2:30)
> *(Show either the README architecture diagram or talk through the sidebar specs)*
>
> *"Let us briefly examine PolyBot's RAG architecture:*
> 1. ***Data Preprocessing & Embedding Model***: *Our raw policy texts are cleaned and embedded using `sentence-transformers/all-MiniLM-L6-v2`, running via ONNX Runtime for high-speed, lightweight dense vector generation with 384 dimensions.*
> 2. ***Vector Database***: *We use **ChromaDB** with Cosine similarity indexing to store document embeddings alongside rich metadata such as document title and source reference.*
> 3. ***Orchestration Framework***: *We utilize **LangChain** to handle the prompt pipeline, multi-turn conversational history, and strict system guardrails.*
> 4. ***Language Model***: *For generation, we connect to **Groq Cloud API** running open models like `gpt-oss-20b` or `llama3`. We set the temperature strictly to 0 to prevent hallucinations and enforce factual accuracy.*
> 5. ***Frontend***: *The entire interface is built with **Streamlit** and deployed publicly on Streamlit Community Cloud."*

---

### Part 3: Live Walkthrough of Deployed App (2:30 – 3:45)
> *(Show the browser with your public Streamlit URL)*
>
> *"Here is our live deployed application. Notice that anyone with this public link can open the application instantly with **no login required** and without installing any software.*
>
> *On the left sidebar, users can see the system architecture, model selector, clear chat history button, and our **Free-Tier Usage Limit Notice**, which informs users about the 30 requests-per-minute rate limit on the Groq free tier.*
>
> *In the main window, we have quick-prompt buttons for common inquiries and an intuitive conversational interface."*

---

### Part 4: Live Query Demonstrations (3:45 – 6:00)

#### Demonstration 1: Eligibility & Income Ceiling
> *(Click the button or type: "What are the eligibility requirements for the CHED Merit Scholarship, especially the income limit?")*
>
> *"Let's test our first query: 'What are the eligibility requirements for the CHED Merit Scholarship, especially the income limit?'*
>
> *(Wait 1-2 seconds for response)*
>
> *As you can see, PolyBot accurately answers that applicants must be Filipino citizens, graduating high school seniors or graduates with a minimum GWA of 93%, and that the combined annual gross income of parents must not exceed PHP 500,000.*
>
> *Notice our grounding feature: clicking the **'Retrieved Sources & Grounding Passages'** expander reveals the exact source—CHED Merit Scholarship Program Guidelines—along with the cosine distance and the raw excerpt used to formulate the answer."*

#### Demonstration 2: Documentary Requirements
> *(Type: "What documentary proofs do I need to prepare to prove my parents' income?")*
>
> *"Now let's ask a more specific follow-up: 'What documentary proofs do I need to prepare to prove my parents' income?'*
>
> *(Show response)*
>
> *PolyBot cites the documentary requirements: latest Income Tax Return (ITR), BIR Certificate of Tax Exemption, DSWD Certificate of Indigence, or OFW contract. Again, the source passage is clearly traceable."*

#### Demonstration 3: Out-of-Scope Query (Anti-Hallucination Test)
> *(Click the 'Out-of-Scope Test' button or type: "How do I apply for a NASA astronaut pilot spaceflight grant?")*
>
> *"Now, as required by the semester guidelines, let's ask a question that the knowledge base CANNOT answer: 'How do I apply for a NASA astronaut pilot spaceflight grant?'*
>
> *(Show response)*
>
> *Notice PolyBot's disciplined refusal: 'I do not have enough verified information in my knowledge base to answer this question. Please consult the official CHED Regional Office (CHEDRO) or the campus scholarship office.'*
>
> *PolyBot does NOT hallucinate or make up rules; it strictly adheres to our anti-hallucination guardrail."*

---

### Part 5: Limitations & Future Improvements (6:00 – 7:00)
> *"To conclude our presentation, here are the key improvements we plan for future iterations:*
> 1. ***Direct PDF & Image Ingestion***: *Adding OCR (Optical Character Recognition) so students can upload scanned flyers or PDF announcements directly.*
> 2. ***Multi-lingual / Tagalog & Bisaya Support***: *Expanding prompt instructions to answer fluently in regional Filipino languages.*
> 3. ***School Portal Integration***: *Connecting PolyBot to university student information systems so students can directly check their GWA eligibility in real time.*
>
> *Thank you very much for watching our demonstration! All source code, documentation, and setup instructions are publicly accessible on our GitHub repository."*

---

## ⚠️ Final Submission Reminder:
1. Upload this video to **Google Drive** or **YouTube (Unlisted)**.
2. In Google Drive: Right-click the video $\to$ **Share** $\to$ set General access to **"Anyone with the link (Viewer)"**.
3. **Open the link in an Incognito / Private window** to make 100% sure it opens without requiring permission! (Avoid the -10 point automatic deduction).
