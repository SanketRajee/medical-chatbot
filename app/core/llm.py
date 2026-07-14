from operator import itemgetter

from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import GOOGLE_API_KEY, INDEX_NAME
from app.core.helper import download_embeddings
from app.core.prompt import system_prompt


def format_docs(docs):
    """Join retrieved documents into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain():
    """
    Build and return the full RAG (Retrieval-Augmented Generation) chain.

    Steps:
      1. Load HuggingFace embeddings
      2. Connect to the Pinecone vector store
      3. Create a retriever that fetches the top-3 similar documents
      4. Initialize the Gemini LLM
      5. Assemble the chain: retrieve → format → prompt → LLM → parse
    """

    # Step 1: Load embeddings model
    print("Loading HuggingFace embeddings...")
    embeddings = download_embeddings()

    # Step 2: Connect to existing Pinecone index
    print("Connecting to Pinecone index...")
    vector_store = PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=embeddings
    )

    # Step 3: Create retriever (top-3 similar chunks)
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    # Step 4: Initialize Gemini LLM
    print("Initializing Gemini LLM...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY
    )

    # Step 5: Build the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # Step 6: Assemble the full RAG chain using LCEL
    # Input expected: {"input": "user question string"}
    # Flow: extract string → retrieve docs → build prompt → LLM → plain string
    rag_chain = (
        {
            "context": itemgetter("input") | retriever | format_docs,
            "input":   itemgetter("input")
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print("RAG chain ready!")
    return rag_chain
