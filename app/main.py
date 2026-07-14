from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
from app.core.llm import build_rag_chain

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: build the RAG chain and store in app state
    print("Starting up — initializing RAG chain...")
    app.state.rag_chain = build_rag_chain()
    print("Startup complete.")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(title="Medical AI Assistant API", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

from app.api.chat import router as chat_router  # noqa: E402
app.include_router(chat_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)
