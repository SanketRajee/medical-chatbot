from langchain_huggingface import HuggingFaceEmbeddings


def download_embeddings():
    """
    Load and return the HuggingFace sentence-transformer embeddings model.
    Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
    Must match the dimension of the Pinecone index.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings
