# RAG-PDF-Search

A retrieval-augmented generation (RAG) system that extracts text from PDF files, embeds them with OpenAI embeddings, indexes them in a FAISS vector store, and answers natural-language questions using GPT.

## Repository Structure

```
.
├── configs/
│   └── config.py         # Environment-based configuration
├── src/
│   ├── embedder.py        # Text embedding via OpenAI (text-embedding-3-small)
│   ├── extraction_schema.py  # Regex-based metadata extraction
│   ├── llm_client.py      # GPT query client with retry logic
│   ├── main.py            # Interactive CLI entry point
│   ├── pdf_loader.py      # PDF extraction, cleaning, and chunking
│   ├── pipeline.py        # End-to-end build & query pipeline
│   └── vector_store.py    # FAISS vector store wrapper
├── tests/                 # Pytest suite for pure-logic components
├── requirements.txt
├── requirements-dev.txt   # Dev/test-only dependencies (pytest)
└── scalability.md         # Notes on scaling to 10k+ PDFs
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/pesala111/hybrid-rag-pdf-search.git
cd hybrid-rag-pdf-search
```

### 2. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root (this file is gitignored and never committed):

```
OPENAI_API_KEY=sk-...your-key-here...
DATA_ZIP=/absolute/path/to/your/sample dataset.zip
```

Alternatively, export them in your shell:

```bash
export OPENAI_API_KEY="sk-...your-key-here..."
export DATA_ZIP="/absolute/path/to/your/sample dataset.zip"
```

**Never hard-code your API key in source files or commit it to version control.**

### 4. Run the demo

```bash
python -m src.main
```

You should see:

```
❓ Ask a question:
```

Type a question such as:

```
What is the color temperature of the SIRIUS HRI 330W?
```

and press Enter. The system will extract and chunk the PDFs (once per run), build FAISS embeddings, retrieve the most relevant chunks, and answer your question using the LLM. Type `exit` or `quit` to stop.

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `DATA_ZIP` | `data/sample dataset.zip` | Path to the ZIP file containing PDFs |
| `EXTRACT_DIR` | system temp dir | Directory to extract PDFs into |
| `TOP_K` | `5` | Number of chunks retrieved per query |
| `LLM_MODEL` | `gpt-4o-mini` | OpenAI chat model to use |

## Running Tests

This project includes a small pytest suite covering the pure-logic components (text chunking, metadata extraction, and the FAISS vector store wrapper). These tests do not call the OpenAI API.

```bash
pip install -r requirements-dev.txt
pytest
```

## Scalability

See [`scalability.md`](scalability.md) for a detailed discussion of how this system could be scaled to 10,000+ PDFs.
