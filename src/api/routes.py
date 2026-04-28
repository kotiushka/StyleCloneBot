from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.db import repository
from src.models.schemas import PersonCreate, PersonResponse, UserMessage
from src.services.llm_service import generate_reply

router = APIRouter()


@router.post("/chat")
async def read_users(message: UserMessage, db: AsyncSession = Depends(get_db)):
    # find or create an user
    user = await repository.get_or_create_user(
        db=db,
        telegram_id=message.user_id,
        username=message.username,
        first_name=message.first_name
    )
    
    person = await repository.get_person_by_user(db=db, user_id=user.id)
    if not person:
        raise HTTPException(status_code=400, detail="Сначала загрузи переписку")
    
    example_messages = await repository.get_person_messages(db=db, person_id=person.id, limit=50)

    # save user's message
    await repository.save_message(
        db=db,
        user_id=user.id,
        role="user",
        content=message.message_text
    )

    # get history
    history = await repository.get_history(db=db, user_id=user.id)

    # get a response from openAI
    reply = await generate_reply(message, history, mirror_user_name=person.name, example_messages=example_messages)

    # save bot's message
    await repository.save_message(
        db=db,
        user_id=user.id,
        role="assistant",
        content=reply
    )

    return {"response": reply}


@router.post("/persons")
async def create_person(data: PersonCreate, db: AsyncSession = Depends(get_db)):
    user = await repository.get_or_create_user(
        db=db,
        telegram_id=data.user_id,
        username=data.username,
        first_name=data.first_name
    )
    person = await repository.create_person(
        db=db,
        user_id=user.id,
        name=data.name,
        from_id=data.from_id
    )
    await repository.save_person_messages(
        db=db,
        person_id=person.id,
        messages=data.messages
    )
    return PersonResponse(person_id=person.id)

@router.get("/health")
async def health():
    return {"status": "ok"}