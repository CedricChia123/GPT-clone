from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from server.schema.responses import APIError
from .database import init_db, off_db
from .routes.conversations import router as ConversationRouter
from .routes.queries import router as QueryRouter

app = FastAPI()
app.include_router(ConversationRouter, tags=["Conversations"], prefix="/conversations")
app.include_router(QueryRouter, tags=["LLM Queries"], prefix="/queries")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=APIError(
            code=400,
            message="Invalid Parameters Provided.",
            request={"method": request.method, "url": str(request.url)},
            details={"errors": exc.errors()},
        ).model_dump(),
    )


@app.on_event("startup")
async def start_db():
    await init_db()


@app.on_event("shutdown")
async def close_db():
    await off_db()
