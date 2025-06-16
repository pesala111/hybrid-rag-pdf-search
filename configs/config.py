import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1] 

# Paths
DATA_DIR = ROOT / "data"
DATA_ZIP = "path to your dataset zip file"
EXTRACT_DIR = os.getenv("EXTRACT_DIR", Path(tempfile.gettempdir()) / "pdf_dataset")

# Models & retrieval
TOP_K           = int(os.getenv("TOP_K",5))

# API key
OPENAI_API_KEY  = "path to your openai api key file"

