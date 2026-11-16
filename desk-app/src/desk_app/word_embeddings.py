import re
import zlib

from langchain_core.embeddings import Embeddings

COMMON = {"a", "an", "and", "are", "can", "do", "does", "for", "how", "i",
          "if", "is", "it", "my", "of", "on", "the", "to", "what", "with", "you", "your"}


class WordEmbeddings(Embeddings):
    """Toy embeddings: hash each non-common word into one of 256 buckets. No API key needed."""

    def embed_query(self, text):
        vector = [0.0] * 256
        for word in re.findall(r"[a-z]+", text.lower()):
            if word not in COMMON:
                vector[zlib.crc32(word.rstrip("s").encode()) % 256] += 1.0
        return vector

    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]
