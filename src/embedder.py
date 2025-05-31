import os
from typing import List
from openai import OpenAI
from configs.config import OPENAI_API_KEY, EMBEDDING_MODEL
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_texts(texts: List[str]) -> List[List[float]]:
    from openai import OpenAI
    response = client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002"),
        input=texts
    )
    return [data.embedding for data in response.data]



"""
if __name__ == "__main__":
    print("Running embedder test...")
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Color temperature of the lamp is 6500K."
    ]
    embeddings = embed_texts(sample_texts)
    print(f"Got {len(embeddings)} embeddings.")
    print("First vector (truncated):", embeddings[0][:10], "...")
"""