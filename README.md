# Medical AI Chatbot

A RAG-based medical question-answering chatbot powered by **Google Gemini**, **Pinecone**, and **FastAPI**.

## How It Works

1. User asks a medical question via the chat UI
2. The question is embedded using HuggingFace (`all-MiniLM-L6-v2`)
3. The top-3 most relevant chunks are retrieved from Pinecone
4. Gemini (`gemini-2.5-flash`) answers using only the retrieved context

## Project Structure

```
medical-chatbot/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── api/
│   │   └── chat.py      # Route handlers (GET / and POST /chat)
│   ├── core/
│   │   ├── config.py    # Loads API keys from .env
│   │   ├── helper.py    # HuggingFace embeddings loader
│   │   ├── llm.py       # Builds the RAG chain
│   │   └── prompt.py    # System prompt for the LLM
│   ├── templates/
│   │   └── index.html   # Chat UI
│   └── static/
│       ├── style.css    # UI styles
│       └── script.js    # Frontend chat logic
├── .env                 # API keys (not committed)
└── requirements.txt     # Python dependencies
```

## Setup & Run

```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API keys to .env
PINECONE_API_KEY="your-pinecone-key"
GOOGLE_API_KEY="your-gemini-key"

# 4. Run the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 5000
```

## Using Docker

If you have Docker installed, you can easily containerize and run the application without installing Python locally.

```bash
# 1. Build the Docker image
docker build -t medical-chatbot .

# 2. Run the container (Make sure you pass your API keys!)
docker run -p 5000:5000 \
  -e PINECONE_API_KEY="your-pinecone-key" \
  -e GOOGLE_API_KEY="your-gemini-key" \
  medical-chatbot
```

Or, if you have your `.env` file set up locally, you can use it directly:

```bash
docker run -p 5000:5000 --env-file .env medical-chatbot
```

Open **http://localhost:5000** in your browser.