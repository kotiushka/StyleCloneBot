from fastapi import APIRouter

from src.models.schemas import UserMessage

from src.services.llm_service import generate_reply 

router = APIRouter()


@router.post("/chat")
async def read_users(message: UserMessage):
    result = await generate_reply(message)
    return {"response": result}

@router.get("/health")
async def health():
    return {"status": "ok"}