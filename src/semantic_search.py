import numpy as np
from sentence_transformers import SentenceTransformer
from src.loader import load_embeddings
model = SentenceTransformer('./model/all-MiniLM-L6-v2')

def get_embeddings(title: str):
    return model.encode([title])

def get_similar_score(seed_embedding, source_embedding: list = load_embeddings()):
    # Return index of NRs with highest similarity to seed
    return np.round(np.inner(seed_embedding, source_embedding)[0]*100, 1)

def get_similar_indices(seed_embedding, source_embedding: list = load_embeddings(), top_n: int = 5):
    # Return index of NRs with highest similarity to seed
    return np.inner(seed_embedding, source_embedding).argsort()[0][::-1][:top_n]

