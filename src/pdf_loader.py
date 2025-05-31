import os
import zipfile
import shutil
import re
import logging
from typing import List, Dict
import pdfplumber
from configs.config import DATA_ZIP, EXTRACT_DIR

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
        line = line.replace('\u00A0', ' ')  # Normalize non-breaking space
        line = re.sub(r'\s+', ' ', line).strip()
        line = re.sub(r'^[-•*_]+\s*', '', line)  # Remove leading bullet hyphens/dots/etc.

        # Skip boilerplate headers/footers
        if re.search(r'product datasheet', line, re.IGNORECASE):
            continue
        if re.search(r'©.*osram.*all rights reserved', line, re.IGNORECASE):
            continue
        if re.search(r'page \d+ of \d+', line, re.IGNORECASE):
            continue
        if re.search(r'\b\d{4},\s*\d{2}:\d{2}:\d{2}', line):  # timestamps
            continue

        if not line:
            continue  # skip empty lines

        if buffer:
            buffer += " " + line
        else:
            buffer = line

        # If line ends with sentence-ending punctuation or is a clear key-value or title line, flush it
        if re.search(r'[.:;!?]$', line) or ':' in line or re.match(r'^[A-Z].*$', line):
            cleaned_lines.append(buffer.strip())
            buffer = ""

    # Add any leftover buffer
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

    structured_text = "\n".join(all_lines)      # readable format for LLM
    embedding_text = " ".join(all_lines)        # continuous format for vector store

    return {
        "structured": structured_text.strip(),
        "embedding": embedding_text.strip()
    }


def load_and_chunk_pdfs() -> List[Dict]:
    extract_zip(DATA_ZIP, EXTRACT_DIR)
    chunks: List[Dict] = []

    for root, _, files in os.walk(EXTRACT_DIR):
        for fname in files:
            if not fname.lower().endswith('.pdf'):
                continue
            if fname.startswith("._") or "__MACOSX" in root:
                continue

            path = os.path.join(root, fname)
            try:
                text_obj = extract_text(path)
                chunks.append({
                    "content": text_obj["structured"],
                    "content_for_embedding": text_obj["embedding"],
                    "metadata": {"source": fname, "chunk_index": 0}
                })
            except Exception as e:
                print(f"⚠️ Skipping '{fname}' due to error: {e}")

    return chunks


if __name__ == "__main__":
    chunks = load_and_chunk_pdfs()
    if chunks:
        print("\n📄 Extracted chunk 1 preview:\n" + "-" * 40)
        print(chunks[0]["content"][:4000])
        print("\n🧾 Metadata:", chunks[0]["metadata"])
    else:
        print("⚠️ No chunks extracted.")
