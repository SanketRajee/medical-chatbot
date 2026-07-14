from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent  # points to app/
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@router.post("/chat")
async def chat(request: Request, msg: str = Form(...)):
    print(f"User Question: {msg}")
    rag_chain = request.app.state.rag_chain
    answer = rag_chain.invoke({"input": msg})
    print(f"Bot Response: {answer}")
    return {"answer": answer}

