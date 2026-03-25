import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from app.core.config import settings
from app.rag.policies import POLICY_DOCS

client = chromadb.PersistentClient(path="/chroma")

embedding_fn = OpenAIEmbeddingFunction(
    api_key=settings.openai_api_key,
    model_name="text-embedding-3-small",
)

collection = client.get_or_create_collection(
    name="shiftpilot_policies",
    embedding_function=embedding_fn,
)


def seed_policy_collection() -> None:
    collection.upsert(
        ids=[doc["id"] for doc in POLICY_DOCS],
        documents=[doc["document"] for doc in POLICY_DOCS],
        metadatas=[doc["metadata"] for doc in POLICY_DOCS],
    )


def retrieve_policies(query: str, n_results: int = 3) -> list[str]:
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )
    return results.get("documents", [[]])[0]