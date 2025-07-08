***Document Reader QNA and Question answer evalution***

# Deployed on streamlit 

https://document001qna.streamlit.app/

A Streamlit-based application that allows users to upload documents (PDF, Word, TXT) and performs two primary functions:

1. **Summarization:** Uses LangChain and Perplexity API to generate concise summaries of uploaded documents.
2. **Question & Answer:** Enables users to ask questions about document content, powered by a LangChain-driven Q\&A chain.

---

## 🚀 Features

* **Multi-format Support:** Upload PDF, Word (`.docx`), or plain text files.
* **Efficient Summarization:** Generate accurate summaries using advanced LLMs.
* **Interactive Q\&A:** Ask questions in natural language and get context-aware answers.
* **Two Interaction Modes:**

  * **Ask Anything:** Freestyle Q\&A over the document.
  * **Challenge Me:** System-generated logic questions for self-assessment.
* **Persistent Vector Store:** Stores embeddings in Chroma for fast retrieval and context maintenance.
* **Admin & User Views:** Separate interfaces for end-users and administrators.

---

## 📦 Tech Stack

* **Framework:** Streamlit
* **LLM Orchestration:** LangChain
* **Embeddings & Vector Store:** OpenAI embeddings, Chroma vector database
* **APIs:** Perplexity API for summarization and Q\&A
* **Storage:** Local file system for uploads, Chroma for vectors
* **Frontend:** HTML & CSS within Streamlit

---

## 💡 Architecture Overview

1. **File Upload:** User uploads a document via Streamlit UI.
2. **Text Extraction:** Documents are parsed and text is extracted.
3. **Embedding Generation:** Extracted text is chunked and converted to embeddings.
4. **Vector Store:** Embeddings stored in Chroma for semantic retrieval.
5. **Summarization:** User triggers summary generation; Perplexity API and LangChain produce a summary.
6. **Q\&A:** User questions are embedded, matched against stored chunks, and answered by the LLM.
7. **Modes:** "Challenge Me" mode generates logic questions based on content.

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/DarkMatter1217/Document-summarizer-and-QNA.git
   cd Document-summarizer-and-QNA
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**

   * Create a `.env` file or set environment variables for:

     ```ini
     OPENAI_API_KEY=your_openai_key
     PERPLEXITY_API_KEY=your_perplexity_key
     ```

5. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## 📈 Usage

1. Navigate to [http://localhost:8501](http://localhost:8501) in your browser.
2. Upload a document in the sidebar.
3. Select **Summarize** or **Ask Anything** or **Challenge Me**.
4. For Q\&A, enter your question in the input box and press **Submit**.
5. Review answers or logic questions generated.

---
