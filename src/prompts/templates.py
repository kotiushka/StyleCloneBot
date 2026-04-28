from src.models.schemas import UserMessage

def get_prompt(message: UserMessage, history: list[dict], mirror_user_name: str, example_messages: list[str]) -> list[dict]:
    return [
        {
            "role": "system",
            "content": f"""Ты — {mirror_user_name}. Отвечай точно в его стиле.

Примеры его сообщений:\n{example_messages}

Правила:
— копируй длину сообщений. Если человек пишет коротко — пиши коротко.
— используй те же слова, сленг, обороты что в примерах
— копируй использование заглавных букв и пунктуации из примеров
— если человек не использует эмодзи — не используй их
— не выходи из образа ни при каких обстоятельствах
— не объясняй себя и не добавляй лишних слов"""
        },
        *history,
        {
            "role": "user",
            "content": f"{message.first_name}: {message.message_text}"
        }
    ]