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
logger = logging.getLogger(__name__)

# Chunking configuration
CHUNK_SIZE = 500    # target characters per chunk
CHUNK_OVERLAP = 100  # overlap between consecutive chunks


def extract_zip(zip_path: str, extract_to: str) -> None:
        """Extract a ZIP archive to the given directory, replacing any existing content."""
        if os.path.exists(extract_to):
                    shutil.rmtree(extract_to)
                os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(path=extract_to)


def clean_text_lines(lines: List[str]) -> List[str]:
        """Normalise and filter raw PDF text lines."""
    cleaned_lines = []
    buffer = ""

    for line in lines:
                line = line.replace("\u00A0", " ")
                line = re.sub(r"\s+", " ", line).strip()
                line = re.sub(r"^[-\u2022*_]+\s*", "", line)

        # Skip boilerplate
                if re.search(
                                r"product datasheet|\u00a9.*osram.*all rights reserved|page \d+ of \d+|\b\d{4},\s*\d{2}:\d{2}:\d{2}",
                                line,
                                re.IGNORECASE,
                ):
                                continue
                            if not line:
                                            continue

        if buffer:
                        buffer += " " + line
else:
            buffer = line

        if re.search(r"[.:;!?]$", line) or ":" in line or re.match(r"^[A-Z].*$", line):
                        cleaned_lines.append(buffer.strip())
                        buffer = ""

    if buffer:
                cleaned_lines.append(buffer.strip())

    return cleaned_lines


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
        """Split text into overlapping fixed-size chunks.

            Args:
                    text: The full document text to split.
                            chunk_size: Approximate character count per chunk.
                                    overlap: Number of characters to repeat between adjacent chunks.

                                        Returns:
                                                A list of text chunks.
                                                    """
    if not text:
                return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
                end = min(start + chunk_size, text_len)
        # Try to break at a sentence boundary
        if end < text_len:
                        boundary = max(
                                            text.rfind(". ", start, end),
                                            text.rfind("\n", start, end),
                        )
                        if boundary > start:
                                            end = boundary + 1  # include the period/newline
        chunks.append(text[start:end].strip())
        start = end - overlap if end - overlap > start else end

    return [c for c in chunks if c]


def extract_text(pdf_path: str) -> Dict[str, str]:
        """Extract and clean text from a single PDF file."""
    all_lines: List[str] = []

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
                "extracted_metadata": extracted_meta,
    }


def load_and_chunk_pdfs() -> List[Dict]:
        """Extract PDFs from the ZIP, chunk each document, and return a flat list of chunks."""
    extract_zip(DATA_ZIP, EXTRACT_DIR)
    chunks: List[Dict] = []
    chunk_counter = 0

    for root, _, files in os.walk(EXTRACT_DIR):
                for fname in files:
                                if not fname.lower().endswith(".pdf") or fname.startswith("._") or "__MACOSX" in root:
                                                    continue

            path = os.path.join(root, fname)
            try:
                                text_obj = extract_text(path)
                doc_chunks = chunk_text(text_obj["structured"])

                if not doc_chunks:
                                        logger.warning("No text extracted from '%s'; skipping.", fname)
                                        continue

                for doc_chunk in doc_chunks:
                                        chunks.append({
                                                                    "content": doc_chunk,
                                                                    "content_for_embedding": doc_chunk,
                                                                    "metadata": {
                                                                                                    "source": fname,
                                                                                                    "chunk_index": chunk_counter,
                                                                                                    "extracted_fields": text_obj["extracted_metadata"],
                                                                    },
                                        })
                                        chunk_counter += 1

except Exception as e:
                logger.warning("Skipping '%s' due to error: %s", fname, e)

    logger.info("Loaded %d chunks from %s.", chunk_counter, EXTRACT_DIR)
    return chunks


if __name__ == "__main__":
        result = load_and_chunk_pdfs()
    if result:
                for i, chunk in enumerate(result[:3]):
                                print(f"\n Chunk {i + 1} preview:\n" + "-" * 40)
            print(chunk["content"][:1000])
            print("\n Metadata:", chunk["metadata"])
else:
        print("No chunks extracted.")
