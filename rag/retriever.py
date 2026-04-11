import os

class Retriever:
    def __init__(self, data_path="data/knowledge_base"):
        self.data_path = data_path
        self.documents = self.load_documents()

    def load_documents(self):
        docs = []

        # Loop through all files in knowledge_base
        for filename in os.listdir(self.data_path):
            filepath = os.path.join(self.data_path, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                docs.append(f.read())

        return docs

    def get_relevant_docs(self, query):
        results = []
        query_words = query.lower().split()

        for doc in self.documents:
            for word in query_words:
                if word in doc.lower():
                    results.append(doc)
                    break

        return results[:2]