import json
import pickle

def load_nrs():
    with open('./data/results.json', 'rb') as f:
        return json.load(f)

def load_embeddings():
    with open('./data/embeddings.pickle', 'rb') as f:
        return pickle.load(f)