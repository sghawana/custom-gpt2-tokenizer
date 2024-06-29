import os
import pickle

from paths import DATASET_DIRECTORY, SOURCE
from corpus import generate_corpus

from vocab import get_token_pair_counts, merge_tokens, generate_merges
from corpus import generate_corpus

CORPUS_NAME = 'text_corpus.txt'
NUM_MERGES = 50

class Tokenizer:
    def __init__(self) -> None:
        self.vocab = None
        self.special = None
        self.merges = None
        
    @classmethod
    def load(cls, path):
        tokenizer_file = os.path.join(path, "tokenizer.pkl")

        if not os.path.exists(path) or not os.path.exists(os.path.join(path, "tokenizer.pkl")):
            raise ValueError(cls.load.__name__ + ": No tokenizer found at the specified directory")

        with open(tokenizer_file, "rb") as pkl_file:
            return pickle.load(pkl_file)
        
    def save(self, path):
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "tokenizer.pkl"), 'wb') as pkl_file:
            pickle.dump(self, pkl_file)
            
    
    def train(self, corpus, vocab_size):
        ...
        
    def encode(self, string):
        
        encodings = string.encode("utf-8", errors='replace')
        for pair, target in self.merges.items():
            merge_tokens(encodings, pair, target)
            
        return encodings
    
    def decode(self, tokens):
        
        for 
            
        
        
        