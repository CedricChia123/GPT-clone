from fastapi import FastAPI
from .database import init_db
from .routes.conversation import router as Router

app = FastAPI()
app.include_router(Router, tags=["Conversations"], prefix="/conversation")

@app.on_event("startup")
async def start_db():
    await init_db()

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Hello World!"}
