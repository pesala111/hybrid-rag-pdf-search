## 📈 Scalability: How I’d Scale This Project for 10,000+ PDFs

If I had to scale this project to handle 10,000 or more PDFs, here are some points what I would change or improve to keep it fast, accurate, and manageable.

### 1. Swap FAISS with a Real Vector Database

Right now, I’m using FAISS just for local testing, but for a larger setup, I would move to a proper vector DB like **Qdrant**, **Weaviate**, or **Pinecone**. These offer built-in support for:

- Persistent storage
- Metadata filtering
- Scalable APIs

So I wouldn’t have to write all that logic myself.

---

### 2. Preprocess Embeddings Only Once

Currently, text is embedded every time the script runs — which won’t work for 10k PDFs, so I would refactor the pipeline to:

- Extract & embed text once
- Save those vectors + metadata to disk or a DB
- Use that saved data during search

This makes querying much faster and way more efficient.

---

### 3. Use Structured Metadata for Filtering

Since here in this demo project already extracting fields like **wattage**, **lifetime**, **product number**, etc., I’d improve this keyword extraction and use them with efficient filter chunks *before* even doing a vector search.

Example: If a query says “≥1000W and >400hr”, I can narrow it down using just metadata — then embed the query and search only within the filtered results.

I'd also standardize units (W, hr, K) since most datasheets follow similar formats but some with different units as it can be benificial in queries like comparisions or conditional listings.

---

### 4. Store Metadata in a Real Database

Instead of keeping metadata in memory or JSON, I’d store it in a proper DB like **PostgreSQL** or **SQLite**. That way, I can:

- Query and filter easily
- Track which PDF document each chunk came from (for explainability)
- Handle updates or deletions more cleanly (for the new incoming data periodically)

---


### 6. Handle Incremental Updates

With 10k+ PDFs, I wouldn’t want to re-embed everything every time something changes. Instead:

- Track file timestamps in a DB
- Reprocess only new or updated files
- Remove old vectors and add new ones

 This keeps things fresh and clean ways without wasting compute.

---

### 7. Watch for Slow Queries

As data grows, searches can get slower. To keep things fast:

- Shard the vector store
- Group documents by category (e.g., “medical”, “stage lighting” etc depending on the nature of the desired usecase)
- Cache common query results for quick responses

---

### 8. Better Prompts for Better Answers

I’d improve prompt engineering depending on the query type: (only if required)

- Use strict formats for numeric queries
- Force the model to cite source chunks
- Customize instructions for specific information types

---

### 9. Rely More on Metadata for Precision

Many questions (like “What is the color temp of model X?”) are factual instead semantic similarity, so instead of depending on the LLM to infer this from chunk text, I’d rely more on structured metadata for direct answers.

---

### 10. Multi-Stage Retrieval

For complex queries, I’d use a two-step retrieval:

1. Filter chunks using metadata
2. Run vector search only within those
3. Re-rank the top results using an LLM

⚡ This boosts both accuracy and speed.

---

### 11. Manage LLM Context Size

With increasing data, there will be more chunks for queries like "Provide me with all light sources with at least 1000 watts and a lifespan of more than 400 hours.", so it's easy to hit token limits, so I'd handle that by:

- Summarizing long chunks
- Truncating low-relevance ones
- Prioritizing by chunk score

---

### 12. Track What’s Working (and What’s Not)

Monitoring helps guide improvements. I’d track:

- Embedding failures
- Index build durations
- Query latencies
- Retrieval accuracy (i.e. was the correct chunk retrieved?)

---

So overall *do more work up front** (preprocessing, structuring, indexing)  
*So that querying stays fast, accurate, and efficient*, even at large scale.
