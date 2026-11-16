from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

POLICIES = {
    "refunds.md": "Refunds go back to the card you paid with. They take up to 5 working days to arrive."
                  "\n\nYou can ask for a refund within 30 days of delivery. Opened items can be refunded if they are faulty.",
    "shipping.md": "Standard shipping takes 3 to 5 working days. Shipping is free on orders over 50 euros."
                   "\n\nExpress shipping arrives the next working day and costs 9 euros.",
    "accounts.md": "To reset your password, use the reset link on the sign-in page. Support staff never ask for your password.",
}

docs = [Document(page_content=text, metadata={"source": name}) for name, text in POLICIES.items()]
splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=0, add_start_index=True)
chunks = splitter.split_documents(docs)
