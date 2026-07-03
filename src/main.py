import logging
from src.pipeline import build_pipeline, query_pipeline

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def main():
        """Entry point: build the RAG pipeline and start the interactive query loop."""
        store, chunks = build_pipeline()

    while True:
                user_q = input("\n\u2753 Ask a question: ")
                if user_q.strip().lower() in {"exit", "quit"}:
                                print("Goodbye!")
                                break
                            answer = query_pipeline(user_q, store, chunks)
        print("\U0001f4ac", answer)


if __name__ == "__main__":
        main()
