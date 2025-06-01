# pipeline.py
import numpy as np
from openai import OpenAI
from typing import List, Dict
from src.pdf_loader import load_and_chunk_pdfs
from src.embedder import embed_texts
from src.vector_store import FaissVectorStore
from src.llm_client import call_llm_query
from configs.config import TOP_K

def build_pipeline():
    chunks = load_and_chunk_pdfs()
    texts = [c['content_for_embedding'] for c in chunks]
    metadatas = [c['metadata'] for c in chunks]

    embeddings = embed_texts(texts)
    embeddings_np = np.array(embeddings, dtype='float32')

    dim = embeddings_np.shape[1]
    store = FaissVectorStore(dim)
    store.add(embeddings_np, metadatas)
    return store, chunks


def query_pipeline(query: str, store: FaissVectorStore, chunks: List[Dict], top_k: int = TOP_K) -> str:
    q_emb = np.array(embed_texts([query]), dtype='float32')
    results = store.search(q_emb, top_k)
    contexts = [
        f"Source: {res['metadata']['source']}, Score: {res['score']}\n{chunks[res['metadata']['chunk_index']]['content']}"
        for res in results
    ]

    prompt = (
        "You are an assistant. Use the following context to answer the question.\n\nContext:\n"
        + "\n---\n".join(contexts)
        + f"\n\nQuestion: {query}\nAnswer:"
    )

    return call_llm_query(prompt)