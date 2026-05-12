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


def parse_messages(data: dict, from_id: str) -> list[dict]:
    messages = data["messages"]
    result = []

    for i, msg in enumerate(messages):
        if msg.get("type") != "message":
            continue
        if msg.get("from_id") != from_id:
            continue

        text = msg.get("text", "")
        if isinstance(text, list):
            text = "".join(
                part if isinstance(part, str) else part.get("text", "")
                for part in text
            )
        text = text.strip()
        if len(text) < 2:
            continue

        context = None
        if i > 0:
            prev = messages[i - 1]
            if prev.get("type") == "message" and prev.get("from_id") != from_id:
                prev_text = prev.get("text", "")
                if isinstance(prev_text, list):
                    prev_text = "".join(
                        part if isinstance(part, str) else part.get("text", "")
                        for part in prev_text
                    )
                prev_text = prev_text.strip()
                if len(prev_text) >= 2:
                    context = prev_text

        result.append({"content": text, "context": context})

    return result


def load_json(file_bytes: bytes) -> dict:
    return json.loads(file_bytes.decode("utf-8"))
