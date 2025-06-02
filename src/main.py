from src.pipeline import build_pipeline, query_pipeline

store, chunks = build_pipeline()

while True:
    user_q = input("\n❓ Ask a question: ")
    if user_q.lower() in {"exit", "quit"}:
        break
    answer = query_pipeline(user_q, store, chunks)
    print("💬", answer)
