import os
from typing import List
from openai import OpenAI
from configs.config import OPENAI_API_KEY
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=OPENAI_API_KEY)

def embed_texts(texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return [data.embedding for data in response.data]