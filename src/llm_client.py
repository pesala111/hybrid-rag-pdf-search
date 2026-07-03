import os
import time
import logging
from openai import OpenAI, RateLimitError, APIConnectionError, APIStatusError
from configs.config import OPENAI_API_KEY
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


def call_llm_query(prompt: str, retries: int = 3, backoff: float = 2.0) -> str:
        """Send a prompt to the LLM and return the response, with retry on transient errors."""
        model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        for attempt in range(1, retries + 1):
                    try:
                                    resp = client.chat.completions.create(
                                                        model=model,
                                                        messages=[{"role": "user", "content": prompt}],
                                    )
                                    return resp.choices[0].message.content
except RateLimitError as e:
            logger.warning("Rate limit hit on attempt %d/%d: %s", attempt, retries, e)
            if attempt == retries:
                                raise
                            time.sleep(backoff * attempt)
except APIConnectionError as e:
            logger.warning("Connection error on attempt %d/%d: %s", attempt, retries, e)
            if attempt == retries:
                                raise
                            time.sleep(backoff * attempt)
except APIStatusError as e:
            logger.error("API status error (non-retryable): %s", e)
            raise
