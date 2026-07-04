import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]

# Paths
DATA_DIR = ROOT / "data"
DATA_ZIP = os.getenv("DATA_ZIP", str(ROOT / "data" / "sample dataset.zip"))
EXTRACT_DIR = os.getenv("EXTRACT_DIR", str(Path(tempfile.gettempdir()) / "pdf_dataset"))

# Models & retrieval
TOP_K = int(os.getenv("TOP_K", 5))

# API key — loaded from environment variable or .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
      raise EnvironmentError(
                "OPENAI_API_KEY is not set. "
                "Please set it in your .env file or as an environment variable."
      )
