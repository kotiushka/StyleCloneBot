from openai import AsyncOpenAI
from src.config import OPENAI_KEY

client = AsyncOpenAI(api_key=OPENAI_KEY)

async def get_embedding(text: str) -> list[float]:
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

async def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    all_embeddings = []
    chunk_size = 2000
    
    for i in range(0, len(texts), chunk_size):
        chunk = texts[i:i + chunk_size]
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        all_embeddings.extend([item.embedding for item in response.data])
    
    return all_embeddings
