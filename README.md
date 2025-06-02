# RAG-PDF-Search

## Repository Structure

```text
.
├── configs
│   └── config.py
├── data
│   └── dataset coding challenge-20250529T234530Z-1-001.zip
├── requirements.txt
├── scalability.md
└── src
    ├── embedder.py
    ├── extraction_schema.py
    ├── llm_client.py
    ├── main.py
    ├── pdf_loader.py
    ├── pipeline.py
    └── vector_store.py
```

## Getting Started

#### 1. Clone the repository

```bash
git clone https://github.com/pesala111/rag-pdf-search-pesala.git
cd rag-pdf-search
```

#### 2. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Set your OpenAI API key
> Since this is a private repository, OpenAI API is set normally in the config.py, but if it doesn't workout, please change it with valid API in configs/config.py

or do this appraoch:
```bash
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

#### 4. Set the dataset path

In configs/config.py, set the path to your dataset ZIP file by updating the DATA_ZIP variable.

#### 5. Run the demo

```bash
python -m src.main
```

You should see:

```
❓ Ask a question: ·
```

Now you can type something like:
```
What is the color temperature of the SIRIUS HRI 330W 2/CS 1/SKU?
```
and press Enter. The system will:
1. Extract and chunk the PDFs (once).
2. Build FAISS embeddings.
3. Answer your question.
