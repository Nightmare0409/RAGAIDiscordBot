import os
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class Retriever:
    def __init__(self, data_path="data/knowledge_base"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.documents = []
        self.embeddings = []

        # Load documents
        for filename in os.listdir(data_path):
            with open(os.path.join(data_path, filename), "r", encoding="utf-8") as f:
                text = f.read()

                # Split into chunks (by paragraphs)
                chunks = text.split("\n\n")

                for chunk in chunks:
                    if chunk.strip():
                        self.documents.append(chunk.strip())

        # Convert documents to embeddings
        self.embeddings = self.model.encode(self.documents)

        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings))

    def retrieve(self, query, top_k=2):
        query_embedding = self.model.encode([query])

        distances, indices = self.index.search(
            np.array(query_embedding), top_k
        )

        results = [self.documents[i] for i in indices[0]]
        return results