"""Pytest suite for the pure-logic components of the project.

These tests cover text chunking (src.pdf_loader.chunk_text), regex-based
metadata extraction (src.extraction_schema.extract_keywords_with_regex),
and the FAISS vector store wrapper (src.vector_store.FaissVectorStore).

None of these tests call the OpenAI API, so no network access or a real
API key is required. A dummy OPENAI_API_KEY is set below purely so that
importing configs.config (a transitive import of src.pdf_loader) does
not raise at import time.
"""
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENAI_API_KEY", "test-key-for-pytest-only")

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.pdf_loader import chunk_text
from src.extraction_schema import extract_keywords_with_regex
from src.vector_store import FaissVectorStore

def test_chunk_text_empty_string_returns_empty_list():
    assert chunk_text("") == []

def test_chunk_text_shorter_than_chunk_size_returns_single_chunk():
    text = "This is a short sentence."
    assert chunk_text(text, chunk_size=500, overlap=100) == [text]

def test_chunk_text_splits_long_text_with_overlap():
    text = "0123456789" * 5
    chunks = chunk_text(text, chunk_size=20, overlap=5)
    assert chunks == [text[0:20], text[15:35], text[30:50], text[45:50]]
    assert chunks[0][-5:] == chunks[1][:5]
    assert chunks[1][-5:] == chunks[2][:5]

def test_chunk_text_prefers_sentence_boundary_over_hard_cutoff():
    text = (
        "Alpha beta gamma delta epsilon zeta eta theta. "
        "Iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega."
    )
    chunks = chunk_text(text, chunk_size=50, overlap=10)
    assert chunks[0] == "Alpha beta gamma delta epsilon zeta eta theta."

def test_chunk_text_never_returns_empty_or_whitespace_chunks():
    text = "One. Two. Three. Four. Five."
    chunks = chunk_text(text, chunk_size=10, overlap=2)
    assert all(chunk.strip() for chunk in chunks)

def test_extract_keywords_finds_expected_fields():
    text = "Product number 12345678\nNominal wattage 330 W\nColor temperature 6500 K"
    result = extract_keywords_with_regex(text)
    assert result["Product number"] == "12345678"
    assert result["Nominal wattage"] == "330 W"
    assert result["Color temperature"] == "6500 K"

def test_extract_keywords_skips_fields_not_present():
    text = "Nominal wattage 100 W"
    result = extract_keywords_with_regex(text)
    assert "Nominal wattage" in result
    assert "Color temperature" not in result
    assert "Product number" not in result

def test_extract_keywords_returns_empty_dict_for_empty_text():
    assert extract_keywords_with_regex("") == {}

def test_extract_keywords_dimmable_flag_is_captured():
    text = "This lamp is Dimmable and rated at 50 W."
    result = extract_keywords_with_regex(text)
    assert result.get("Dimmable") == "Dimmable"

def test_vector_store_add_and_search_returns_correct_metadata():
    store = FaissVectorStore(dim=4)
    embeddings = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]], dtype="float32")
    metadatas = [{"id": 0}, {"id": 1}, {"id": 2}]
    store.add(embeddings, metadatas)
    query = np.array([[1, 0, 0, 0]], dtype="float32")
    results = store.search(query, top_k=1)
    assert len(results) == 1
    assert results[0]["metadata"]["id"] == 0
    assert results[0]["score"] == 0.0

def test_vector_store_skips_invalid_indices_when_top_k_exceeds_available():
    store = FaissVectorStore(dim=3)
    embeddings = np.array([[1, 0, 0]], dtype="float32")
    metadatas = [{"id": "only"}]
    store.add(embeddings, metadatas)
    query = np.array([[1, 0, 0]], dtype="float32")
    results = store.search(query, top_k=5)
    assert len(results) == 1
    assert results[0]["metadata"]["id"] == "only"

def test_vector_store_handles_multiple_queries_in_one_call():
    store = FaissVectorStore(dim=2)
    embeddings = np.array([[1, 0], [0, 1]], dtype="float32")
    metadatas = [{"id": 0}, {"id": 1}]
    store.add(embeddings, metadatas)
    queries = np.array([[1, 0], [0, 1]], dtype="float32")
    results = store.search(queries, top_k=1)
    assert len(results) == 2
