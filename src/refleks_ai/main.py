
from fastapi import FastAPI
from .routers import diary_router

app = FastAPI(
    title="Refleks AI",
    description="Aplikacja wspierająca terapię CBT z wykorzystaniem agenta AI",
    version="0.1.0"
)

# Dołączenie routera dziennika
app.include_router(diary_router.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Refleks AI"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
