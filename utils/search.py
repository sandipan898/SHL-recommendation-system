import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticSearch:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.data = None
        self.embeddings = None

    def load_data(self, csv_path):
        """Loads CSV and prepares FAISS index from combined text fields."""
        self.data = pd.read_csv(csv_path)

        # Combine relevant columns into one searchable string
        self.data.fillna("", inplace=True)
        self.data['combined'] = (
            self.data['Title'].astype(str) + " " +
            self.data['Description'].astype(str) + " " +
            self.data['Job Levels'].astype(str) + " " +
            self.data['Languages'].astype(str) + " " +
            self.data['Test Type'].astype(str)
        )

        # Encode combined text
        texts = self.data['combined'].tolist()
        self.embeddings = self.model.encode(texts, show_progress_bar=True)

        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings))

    def query(self, user_query, top_k=5):
        """Searches the FAISS index for top_k most similar entries to the query."""
        if not self.index or self.data is None:
            raise ValueError("Index not initialized. Please load data first.")

        query_vec = self.model.encode([user_query])
        distances, indices = self.index.search(np.array(query_vec), top_k)
        results = self.data.iloc[indices[0]].copy()
        results["score"] = distances[0]
        return results
