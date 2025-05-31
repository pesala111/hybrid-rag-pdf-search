# configs/config.py
from pathlib import Path
from dotenv import load_dotenv
import os, tempfile

load_dotenv()                                            # load .env if present

ROOT = Path(__file__).resolve().parents[1]               # repo root

# Paths
DATA_DIR = ROOT / "data"
DATA_ZIP = "/Users/pesala/Downloads/dataset coding challenge-20250530T131432Z-1-001.zip"
EXTRACT_DIR = os.getenv("EXTRACT_DIR", Path(tempfile.gettempdir()) / "pdf_dataset")

# Chunking
CHUNK_SIZE     = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP  = int(os.getenv("CHUNK_OVERLAP", 50))

# Models & retrieval
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
LLM_MODEL       = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
TOP_K           = int(os.getenv("TOP_K", 5))

# Vector store
FAISS_INDEX     = os.getenv("FAISS_INDEX", "IndexFlatL2")

# API key
OPENAI_API_KEY  = "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"