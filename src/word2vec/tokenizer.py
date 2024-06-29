import os
import pickle
import torch

from help_functions import merge_tokens, unmerge_tokens, generate_merges

class Tokenizer:
    def __init__(self) -> None:
        self.vocab = None
        self.special = None
        self.merges = None
        self.device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
        
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
            
    
    def train(self, corpus_path, vocab_size):
        
        with open(corpus_path) as f: corpus = f.read()
        tokens = torch.tensor(list(corpus.encode('utf-8', errors='replace')), dtype=torch.int32, device=self.device)
        
        unique_tokens = torch.unique(tokens)
        vocab = {token.item():i for i,token in enumerate(unique_tokens)}
        num_merges = max(0, vocab_size - len(vocab))
        self.merges = generate_merges(tokens, num_merges)
        
        n = len(vocab)
        for i, new_token in enumerate(self.merges.values()):
            vocab[new_token] = n + i
        self.vocab = vocab
        
    def encode(self, string: str) -> torch.Tensor:
        tokens = torch.tensor(list(string.encode("utf-8", errors='replace')), dtype=torch.int32, device=self.device)
        for pair, target in self.merges.items():
            tokens = merge_tokens(tokens, pair, target)
        return tokens
    
    def decode(self, tokens: torch.Tensor) -> str:
        for pair, target in reversed(list(self.merges.items())):
            tokens = unmerge_tokens(tokens, pair, target)
        string = bytes(tokens.tolist()).decode('utf-8', errors='replace')
        return string
        
        
