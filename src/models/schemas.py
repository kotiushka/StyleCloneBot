from pydantic import BaseModel


class UserMessage(BaseModel):
    user_id: int
    username: str | None = None
    first_name: str 
    message_text: str
    

class PersonCreate(BaseModel):
    user_id: int
    username: str | None = None
    first_name: str
    name: str
    from_id: str
    messages: list[str]


class PersonResponse(BaseModel):
    person_id: int
    