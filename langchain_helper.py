import os
import pickle
import numpy as np
from secret_key import secret_key
from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import anthropic

# Setup
os.environ['ANTHROPIC_API_KEY'] = secret_key

# LLM
llm = ChatAnthropic(model="claude-haiku-4-5")
parser = StrOutputParser()
client = anthropic.Anthropic(api_key=secret_key)

def get_embedding(text):
    # Use Claude to create simple embeddings via hash trick
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        messages=[{"role": "user", "content": f"Reply with only 10 numbers between 0 and 1 separated by commas that represent the semantic meaning of this text: {text[:500]}"}]
    )
    numbers = response.content[0].text.strip().split(",")
    return [float(n.strip()) for n in numbers[:10]]

def process_urls(urls):
    # Step 1 - Load data
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()

    # Step 2 - Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " "],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    docs = text_splitter.split_documents(data)

    # Step 3 - Save docs to pickle
    with open("faiss_store.pkl", "wb") as f:
        pickle.dump(docs, f)

    return f"URLs processed! {len(docs)} chunks created."

def get_answer(question):
    # Load saved docs
    with open("faiss_store.pkl", "rb") as f:
        docs = pickle.load(f)

    # Simple keyword search to find relevant chunks
    question_words = set(question.lower().split())
    scored_docs = []
    for doc in docs:
        content_words = set(doc.page_content.lower().split())
        score = len(question_words & content_words)
        scored_docs.append((score, doc))

    # Get top 3 most relevant chunks
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_docs = [doc for score, doc in scored_docs[:3]]

    context = "\n\n".join([d.page_content for d in top_docs])
    sources = "\n".join([d.metadata.get("source", "") for d in top_docs])

    # Ask Claude
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Use the following information to answer the question.
        If you don't know, say you don't know.

        Context: {context}

        Question: {question}

        Answer:"""
    )

    chain = prompt | llm | parser
    answer = chain.invoke({"context": context, "question": question})

    return {"answer": answer, "sources": sources}