# Import the built-in os module for working with files and directories
import os
# Import numpy for handling arrays and numerical operations
import numpy as np
# Import a pre-trained model for converting text into embeddings (numbers)
from sentence_transformers import SentenceTransformer
# Import FAISS for fast similarity search
import faiss

# Define a class responsible for retrieving relevant text
class Retriever:
    # Initialize the Retriever with a path to the data
    def __init__(self, data_path="data/knowledge_base"):
        # Load a pre-trained sentence embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Create an empty list to store text documents
        self.documents = []
        # Create an empty list to store embeddings (vector representations)
        self.embeddings = []

        # Loop through each file in the specified directory
        for filename in os.listdir(data_path):
            # Open each file in read mode with UTF-8 encoding
            with open(os.path.join(data_path, filename), "r", encoding="utf-8") as f:
                # Read the entire content of the file
                text = f.read()

                # Split the text into chunks using double newlines (paragraphs)
                chunks = text.split("\n\n")

                # Loop through each chunk
                for chunk in chunks:
                    # Check if the chunk is not empty after stripping spaces
                    if chunk.strip():
                        # Add the cleaned chunk to the documents list
                        self.documents.append(chunk.strip())

        # Convert all documents into embeddings (numeric vectors)
        self.embeddings = self.model.encode(self.documents)

        # Get the dimension size of the embeddings
        dimension = self.embeddings.shape[1]
        # Create a FAISS index for similarity search using L2 distance
        self.index = faiss.IndexFlatL2(dimension)
        # Add embeddings into the FAISS index
        self.index.add(np.array(self.embeddings))

    # Define a method to retrieve relevant documents based on a query
    def retrieve(self, query, top_k=2):
        # Convert the query into an embedding
        query_embedding = self.model.encode([query])

        # Search the FAISS index for the closest matches
        distances, indices = self.index.search(
            np.array(query_embedding), top_k
        )

        # Collect the matching documents using the returned indices
        results = [self.documents[i] for i in indices[0]]
        # Return the retrieved documents
        return results