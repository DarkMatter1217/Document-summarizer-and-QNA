import streamlit as st
from io import BytesIO
from summarizer import summarize_with_perplexity
from qa import (
    build_vector_store,
    answer_question,
    generate_questions,
    evaluate_user_answer
)

from PyPDF2 import PdfReader

st.set_page_config(page_title="Smart Research Assistant", layout="centered")
st.title("📄 Smart Assistant for Research Summarization")

uploaded_file = st.file_uploader("Upload a PDF or TXT document", type=["pdf", "txt"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    buffered_file = BytesIO(uploaded_file.read())

    with st.spinner("Extracting text..."):
        try:
            if uploaded_file.name.endswith(".pdf"):
                reader = PdfReader(buffered_file)
                text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
            elif uploaded_file.name.endswith(".txt"):
                text = buffered_file.read().decode("utf-8")
            else:
                st.error("Unsupported file type!")
                st.stop()
        except Exception as e:
            st.error(f"Error reading document: {e}")
            st.stop()

    if text:
        st.subheader("📜 Extracted Text Preview")
        st.text_area("Document Content", text[:2000] + "...", height=300)

        with st.spinner("Generating summary..."):
            try:
                summary = summarize_with_perplexity(text)
                st.subheader("🔍 Auto Summary (≤ 150 words)")
                st.write(summary)
            except Exception as e:
                st.error(f"Summarization failed: {e}")

        with st.spinner("Indexing document for Q&A..."):
            try:
                vectordb = build_vector_store(text)
            except Exception as e:
                st.error(f"Vector store creation failed: {e}")
                st.stop()

        st.subheader("💬 Ask Anything from Document")
        user_question = st.text_input("Ask a question:")
        if user_question:
            with st.spinner("Thinking..."):
                try:
                    answer, reference = answer_question(vectordb, user_question)
                    st.markdown("**Answer:**")
                    st.write(answer)
                    with st.expander("📌 Show Reference Snippets"):
                        st.code(reference)
                except Exception as e:
                    st.error(f"Error: {e}")

        st.subheader("🧠 Challenge Me")

        if st.button("Generate Logic-Based Questions"):
            with st.spinner("Generating questions..."):
                try:
                    questions_text = generate_questions(text)
                    questions_list = [
                        q.strip().split(". ", 1)[-1]
                        for q in questions_text.strip().split("\n")
                        if q.strip()
                    ]
                    st.session_state["challenge_questions"] = questions_list
                except Exception as e:
                    st.error(f"Error generating questions: {e}")

        if "challenge_questions" in st.session_state:
            st.markdown("#### Your Turn:")
            user_answers = []
            for i, question in enumerate(st.session_state["challenge_questions"]):
                st.markdown(f"**Q{i+1}: {question}**")
                answer = st.text_input(f"Your answer for Q{i+1}:", key=f"ans{i}")
                user_answers.append((question, answer))

            if st.button("Evaluate Answers"):
                st.subheader("📊 Evaluation Results")
                for q, a in user_answers:
                    if a.strip():
                        with st.spinner(f"Evaluating Q: {q}"):
                            try:
                                result = evaluate_user_answer(vectordb, q, a)
                                st.markdown(f"**Q:** {q}")
                                st.markdown(f"**Your Answer:** {a}")
                                st.markdown(f"**Feedback:** {result}")
                                st.markdown("---")
                            except Exception as e:
                                st.error(f"Error evaluating: {e}")
    else:
        st.warning("❗ No text was extracted from the uploaded file.")
