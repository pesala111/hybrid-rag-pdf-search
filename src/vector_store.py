import faiss
import numpy as np
from typing import List, Dict, Any


class FaissVectorStore:
        def __init__(self, dim: int):
                    self.dim = dim
                    self.index = faiss.IndexFlatL2(dim)
                    self.metadatas: List[Dict[str, Any]] = []

        def add(self, embeddings: np.ndarray, metadatas: List[Dict[str, Any]]):
                    """Add embeddings and their associated metadata to the index."""
                    self.index.add(embeddings)
                    self.metadatas.extend(metadatas)

        def search(self, query_vec: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
                    """Search for top_k nearest neighbours; skips invalid FAISS indices (-1)."""
                    D, I = self.index.search(query_vec, top_k)
                    results = []
                    for dist_list, idx_list in zip(D, I):
                                    for dist, idx in zip(dist_list, idx_list):
                                                        if idx == -1:
                                                                                # FAISS returns -1 when fewer results than top_k exist
                                                                                continue
                                                                            results.append({
                                                            "score": float(dist),
                                                            "metadata": self.metadatas[idx],
                                                        })
                                                return results
