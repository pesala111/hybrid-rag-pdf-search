import time
import logging
from typing import List
from openai import OpenAI, RateLimitError, APIConnectionError, APIStatusError
from configs.config import OPENAI_API_KEY
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_texts(texts: List[str], retries: int = 3, backoff: float = 2.0) -> List[List[float]]:
        """Embed a list of texts using OpenAI embeddings with retry on transient errors."""
        for attempt in range(1, retries + 1):
                    try:
                                    response = client.embeddings.create(
                                                        model=EMBEDDING_MODEL,
                                                        input=texts,
                                    )
                                    return [data.embedding for data in response.data]
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
