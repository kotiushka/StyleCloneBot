import json

def get_participants(data: dict) -> list[dict]:
    
    seen = set()
    participants = []

    for msg in data["messages"]:
        if msg.get("type") != "message":
            continue
        from_id = msg.get("from_id")
        name = msg.get("from")
        if from_id and from_id not in seen:
            seen.add(from_id)
            participants.append({"name": name, "from_id": from_id})

    return participants


def parse_messages(data: dict, from_id: str) -> list[str]:
    messages = []

    for msg in data["messages"]:
        if msg["type"] != "message":
            continue
        if msg["from_id"] != from_id:
            continue

        text = msg["text"]

        if isinstance(text, list):
            text = "".join(
                part if isinstance(part, str) else part.get("text", "")
                for part in text
            )

        text = text.strip()

        if len(text) < 2:
            continue

        messages.append(text)

    return messages


def load_json(file_bytes: bytes) -> dict:
    return json.loads(file_bytes.decode("utf-8"))
