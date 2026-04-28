from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models import User, Message, Person, PersonMessage


async def get_or_create_user(db: AsyncSession, telegram_id: int, username: str | None, first_name: str) -> User:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(telegram_id=telegram_id, username=username, first_name=first_name)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user


async def save_message(db: AsyncSession, user_id: int, role: str, content: str) -> None:
    message = Message(user_id=user_id, role=role, content=content)
    db.add(message)
    await db.commit() 


async def get_history(db: AsyncSession, user_id: int) -> list[dict]:
    result = await db.execute(
        select(Message)
        .where(Message.user_id == user_id)
        .order_by(Message.created_at.desc())
        .limit(15)
    )

    messages = result.scalars().all()
    messages = list(reversed(messages))

    return [{"role": m.role, "content": m.content} for m in messages]


async def create_person(db: AsyncSession, user_id: int, name: str, from_id: str) -> Person:
    person = Person(user_id=user_id, name=name, from_id=from_id)
    db.add(person)
    await db.commit()
    await db.refresh(person)

    return person


async def save_person_messages(db: AsyncSession, person_id: int, messages: list[str]) -> None:
    for content in messages:
        msg = PersonMessage(person_id=person_id, content=content)
        db.add(msg)
    
    await db.commit()


async def get_person_messages(db: AsyncSession, person_id: int, limit: int = 50) -> list[str]:
    result = await db.execute(
        select(PersonMessage)
        .where(PersonMessage.person_id == person_id)
        .limit(limit)
    )
    messages = result.scalars().all()
    
    return [m.content for m in messages]


async def get_person_by_user(db: AsyncSession, user_id: int) -> Person | None:
    result = await db.execute(
        select(Person).where(Person.user_id == user_id)
        .order_by(Person.created_at.desc())
    )
    return result.scalar_one_or_none()


async def get_user_by_telegram_id(db: AsyncSession, telegram_id: int) -> User | None:
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()
