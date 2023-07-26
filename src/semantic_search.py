import numpy as np
from sentence_transformers import SentenceTransformer
from src.loader import load_embeddings

model = SentenceTransformer('./model/all-MiniLM-L6-v2')

def get_embeddings(title: str):
    """
    Given a news release title, returns its embedding using the SentenceTransformer model.

    Args:
        title (str): The title of the news release.

    Returns:
        numpy.ndarray: The embedding of the news release title.
    """
    return model.encode([title])

def get_similar_score(seed_embedding, source_embedding: list = load_embeddings()):
    """
    Given a seed embedding and a list of source embeddings, returns the similarity score between the seed and the most similar embedding.

    Args:
        seed_embedding (numpy.ndarray): The embedding of the seed news release.
        source_embedding (list): A list of embeddings to compare the seed against. Defaults to the embeddings loaded from the data source.

    Returns:
        float: The similarity score between the seed and the most similar embedding, rounded to one decimal place.
    """
    return np.round(np.inner(seed_embedding, source_embedding)[0]*100, 1)

def get_similar_indices(seed_embedding, source_embedding: list = load_embeddings(), top_n: int = 5):
    """
    Given a seed embedding and a list of source embeddings, returns the indices of the top_n most similar embeddings to the seed.

    Args:
        seed_embedding (numpy.ndarray): The embedding of the seed news release.
        source_embedding (list): A list of embeddings to compare the seed against. Defaults to the embeddings loaded from the data source.
        top_n (int): The number of most similar embeddings to return. Defaults to 5.

    Returns:
        numpy.ndarray: The indices of the top_n most similar embeddings to the seed.
    """
    return np.inner(seed_embedding, source_embedding).argsort()[0][::-1][:top_n]

