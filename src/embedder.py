import os
from typing import List
from openai import OpenAI
from configs.config import OPENAI_API_KEY, EMBEDDING_MODEL
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_texts(texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return [data.embedding for data in response.data]


if __name__ == "__main__":
    test_texts = [
        "Primary article identifier: 4062172212311",
        "Product name: SIRIUS HRI 231W 2/CS 1/SKU"
    ]
    vectors = embed_texts(test_texts)
    print(f"Vector size: {len(vectors[0])}, Sample values: {vectors[0][:5]}")
