import os
import zipfile
import shutil
from typing import List, Dict
import pdfplumber
from configs.config import DATA_ZIP, EXTRACT_DIR

import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def extract_zip(zip_path: str, extract_to: str) -> None:
    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(path=extract_to)


def extract_text(pdf_path: str) -> str:
    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text.strip())
    return "\n\n".join(full_text)


def load_and_chunk_pdfs() -> List[Dict]:
    extract_zip(DATA_ZIP, EXTRACT_DIR)
    chunks: List[Dict] = []

    for root, _, files in os.walk(EXTRACT_DIR):
        for fname in files:
            if not fname.lower().endswith('.pdf'):
                continue
            if fname.startswith("._") or "__MACOSX" in root:
                continue  # Skip macOS metadata

            path = os.path.join(root, fname)
            try:
                text = extract_text(path)
                chunks.append({
                    'content': text,
                    'metadata': {'source': fname, 'chunk_index': 0}
                })
            except Exception as e:
                print(f"⚠️ Skipping '{fname}' due to error: {e}")

    return chunks
