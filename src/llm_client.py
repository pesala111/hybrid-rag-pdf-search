import os
from openai import OpenAI
from configs.config import OPENAI_API_KEY
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=OPENAI_API_KEY)

def call_llm(prompt: str) -> str:
    from openai import OpenAI
    resp = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content