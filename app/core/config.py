import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
INDEX_NAME = "medical-chatbot"

if PINECONE_API_KEY:
    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
if GOOGLE_API_KEY:
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
