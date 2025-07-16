
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .routers import diary_router, auth_router, chat_router, ui_router

app = FastAPI(
    title="Refleks AI",
    description="Aplikacja wspierająca terapię CBT z wykorzystaniem agenta AI",
    version="0.1.0"
)

# Montowanie plików statycznych
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dołączenie routerów
app.include_router(auth_router.router)
app.include_router(diary_router.router)
app.include_router(chat_router.router)
app.include_router(ui_router.router)


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
