from langchain_community.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
import os
from dotenv import load_dotenv

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def build_vector_store(doc_text):
    if not doc_text:
        raise ValueError("Document text is empty. Cannot build vector store.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.create_documents([doc_text])

    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(docs, embedding_model)
    return vectordb


def answer_question(vectordb, question, top_k=3):
    relevant_docs = vectordb.similarity_search(question, k=top_k)
    context = "\n---\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""Answer the following question using the provided document context.
Include justification using the source text. Quote reference from the source .Answer clearly using only information provided in the context 
without any citations from external sources. use only text do not use [1] or [2] or [3] etc.
CONTEXT:
{context}

QUESTION:
{question}
"""

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 300
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"], context

def generate_questions(text, num_questions=3):
    prompt = f"""Read the following document and generate {num_questions} logic-based or comprehension-focused questions.

Document:
{text[:4000]}

Output format:
1. Question 1
2. Question 2
3. Question 3
"""

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 400
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def evaluate_user_answer(vectordb, question, user_answer):
    context = "\n---\n".join([doc.page_content for doc in vectordb.similarity_search(question, k=3)])
    prompt = f"""
Given the question and the user's answer, compare it with the document's content and provide feedback.

QUESTION: {question}
USER ANSWER: {user_answer}

Use only the following document context to justify the evaluation.

{context}

Output format:
- Evaluation: (Correct / Partially Correct / Incorrect)
- Feedback: (with justification)
"""

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 400
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
