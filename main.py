import streamlit as st
import langchain_helper

st.title("📰 News Research Tool")
st.sidebar.title("News Article URLs")

url1 = st.sidebar.text_input("URL 1")
url2 = st.sidebar.text_input("URL 2")
url3 = st.sidebar.text_input("URL 3")

process_clicked = st.sidebar.button("Process URLs")

if process_clicked:
    urls = [url for url in [url1, url2, url3] if url]
    with st.spinner("Processing URLs..."):
        result = langchain_helper.process_urls(urls)
    st.success(result)

question = st.text_input("Ask a question about the articles:")

if question:
    with st.spinner("Finding answer..."):
        result = langchain_helper.get_answer(question)
    st.header("Answer")
    st.write(result["answer"])
    st.subheader("Sources")
    st.write(result["sources"])

    