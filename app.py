import streamlit as st
from io import BytesIO
from PyPDF2 import PdfReader
from summarizer import summarize_with_perplexity
from qa import (
    build_vector_store,
    answer_question,
    generate_questions,
    evaluate_user_answer
)

st.set_page_config(page_title="Smart Research Assistant", layout="centered", initial_sidebar_state="auto")
st.title("📄 Text Summarization Chatbot")

uploaded_file = st.file_uploader("Upload a PDF or TXT document", type=["pdf", "txt"])

if uploaded_file:
    if "filename" not in st.session_state or st.session_state["filename"] != uploaded_file.name:
        st.session_state["filename"] = uploaded_file.name
        st.session_state["buffer"] = BytesIO(uploaded_file.read())
        st.session_state.pop("text", None)
        st.session_state.pop("summary", None)
        st.session_state.pop("vectordb", None)
        st.session_state.pop("challenge_questions", None)

    st.success(f"Uploaded: {uploaded_file.name}")

    if "text" not in st.session_state:
        with st.spinner("Extracting text..."):
            try:
                if uploaded_file.name.endswith(".pdf"):
                    reader = PdfReader(st.session_state["buffer"])
                    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
                elif uploaded_file.name.endswith(".txt"):
                    text = st.session_state["buffer"].read().decode("utf-8")
                st.session_state["text"] = text
            except Exception as e:
                st.error(f"Text extraction failed: {e}")
                st.stop()

    if "summary" not in st.session_state:
        with st.spinner("Generating summary..."):
            try:
                st.session_state["summary"] = summarize_with_perplexity(st.session_state["text"])
            except Exception as e:
                st.error(f"Summarization failed: {e}")
                st.stop()

    if "vectordb" not in st.session_state:
        with st.spinner("Indexing document for Q&A..."):
            try:
                st.session_state["vectordb"] = build_vector_store(st.session_state["text"])
            except Exception as e:
                st.error(f"Vector store creation failed: {e}")
                st.stop()

    st.subheader("📜 Extracted Text Preview")
    st.text_area("Document Content", st.session_state["text"][:2000] + "...", height=300)

    st.subheader("📑 Summary")
    st.write(st.session_state["summary"])

    st.subheader("🧠 Choose Interaction Mode")
    mode = st.selectbox("Select Mode", ["Select", "Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        st.subheader("💬 Ask Anything")
        user_question = st.text_input("Ask a question:")
        if user_question:
            with st.spinner("Thinking..."):
                try:
                    answer, reference = answer_question(st.session_state["vectordb"], user_question)
                    st.markdown("**Answer:**")
                    st.write(answer)
                    with st.expander("📌 Show Reference Snippets"):
                        st.markdown(
                            f"""
                            <div style="background-color:#1e1e1e; padding:1rem; border-radius:10px; border:1px solid #444; font-size:0.9rem; line-height:1.6; overflow-x:auto; white-space:pre-wrap; color:white;">
                                {reference.replace('\n', '<br>')}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                except Exception as e:
                    st.error(f"Error: {e}")

    elif mode == "Challenge Me":
        st.subheader("🧠 Challenge Me")

        if "challenge_questions" not in st.session_state:
            with st.spinner("Generating questions..."):
                try:
                    questions_text = generate_questions(st.session_state["text"])
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
                                result = evaluate_user_answer(st.session_state["vectordb"], q, a)
                                st.markdown(f"**Q:** {q}")
                                st.markdown(f"**Your Answer:** {a}")
                                st.markdown(f"**Feedback:** {result}")
                                st.markdown("---")
                            except Exception as e:
                                st.error(f"Error evaluating: {e}")
