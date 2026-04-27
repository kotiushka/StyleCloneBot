from pydantic import BaseModel


class UserMessage(BaseModel):
    user_id: int
    username: str | None = None
    first_name: str 
    message_text: str
    
    mirror_user_name: str
    example_messages: list[str]
