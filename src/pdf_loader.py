import os
import zipfile
import shutil
import re
import logging
from typing import List, Dict
import pdfplumber

from configs.config import DATA_ZIP, EXTRACT_DIR
from src.extraction_schema import extract_keywords_with_regex

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def extract_zip(zip_path: str, extract_to: str) -> None:
    if os.path.exists(extract_to):
        shutil.rmtree(extract_to)
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(path=extract_to)

def clean_text_lines(lines: List[str]) -> List[str]:
    cleaned_lines = []
    buffer = ""

    for line in lines:
        line = line.replace('\u00A0', ' ')
        line = re.sub(r'\s+', ' ', line).strip()
        line = re.sub(r'^[-•*_]+\s*', '', line)

        # Skip boilerplate
        if re.search(r'product datasheet|©.*osram.*all rights reserved|page \d+ of \d+|\b\d{4},\s*\d{2}:\d{2}:\d{2}', line, re.IGNORECASE):
            continue
        if not line:
            continue

        if buffer:
            buffer += " " + line
        else:
            buffer = line

        if re.search(r'[.:;!?]$', line) or ':' in line or re.match(r'^[A-Z].*$', line):
            cleaned_lines.append(buffer.strip())
            buffer = ""

    if buffer:
        cleaned_lines.append(buffer.strip())

    return cleaned_lines

def extract_text(pdf_path: str) -> Dict[str, str]:
    all_lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            raw_text = page.extract_text()
            if not raw_text:
                continue
            lines = raw_text.splitlines()
            cleaned = clean_text_lines(lines)
            all_lines.extend(cleaned)

    structured_text = "\n".join(all_lines)
    embedding_text = " ".join(all_lines)
    extracted_meta = extract_keywords_with_regex(structured_text)

    return {
        "structured": structured_text.strip(),
        "embedding": embedding_text.strip(),
        "extracted_metadata": extracted_meta
    }

def load_and_chunk_pdfs() -> List[Dict]:
    extract_zip(DATA_ZIP, EXTRACT_DIR)
    chunks: List[Dict] = []
    chunk_counter = 0

    for root, _, files in os.walk(EXTRACT_DIR):
        for fname in files:
            if not fname.lower().endswith('.pdf') or fname.startswith("._") or "__MACOSX" in root:
                continue

            path = os.path.join(root, fname)
            try:
                text_obj = extract_text(path)
                chunks.append({
                    "content": text_obj["structured"],
                    "content_for_embedding": text_obj["embedding"],
                    "metadata": {
                        "source": fname,
                        "chunk_index": chunk_counter,
                        "extracted_fields": text_obj["extracted_metadata"]
                    }
                })
                chunk_counter += 1
            except Exception as e:
                print(f"Skipping '{fname}' due to error: {e}")

    return chunks



if __name__ == "__main__":
    chunks = load_and_chunk_pdfs()
    if chunks:
        for i, chunk in enumerate(chunks[:2]):
            print(f"\n Extracted chunk {i + 1} preview:\n" + "-" * 40)
            print(chunk["content"][:4000])
            print("\n Metadata:", chunk["metadata"])
    else:
        print("No chunks extracted.")
