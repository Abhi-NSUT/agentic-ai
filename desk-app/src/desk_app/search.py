from langchain.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from .policies import chunks
from .word_embeddings import WordEmbeddings

store = InMemoryVectorStore(WordEmbeddings())
store.add_documents(chunks)


@tool
def search_policies(query: str) -> str:
    """Search the shop's policies on refunds, shipping and accounts.
    Pass the customer's question, word for word, as the query."""
    found = [doc for doc, score in store.similarity_search_with_score(query, k=2) if score >= 0.3]
    if not found:
        return "No policy covers this."
    return "\n".join(f"[{doc.metadata['source']}] {doc.page_content}" for doc in found)
