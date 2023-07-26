import json
import pickle

def load_nrs():
    """
    Loads news release data from a JSON file.

    Returns:
        A dictionary containing news release data.
    """
    with open('./data/results.json', 'rb') as f:
        return json.load(f)

def load_embeddings():
    """
    Loads pre-trained embeddings from a pickle file.

    Returns:
        A dictionary containing pre-trained embeddings.
    """
    with open('./data/embeddings.pickle', 'rb') as f:
        return pickle.load(f)
