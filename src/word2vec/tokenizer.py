import os
import pickle
import heapq
import torch
import time
from helper_functions import merge_ids, generate_merges


class Tokenizer:
    def __init__(self, device = torch.device('cpu')) -> None:
        self.vocab = {idx : bytes([idx]) for idx in range(256)}
        self.special = None
        self.merges = None
        self.device = device
        self.isTrain = False
        
    @classmethod
    def load(cls, path: str) -> 'Tokenizer':
        tokenizer_file = os.path.join(path, "tokenizer.pkl")
        if not os.path.exists(path) or not os.path.exists(os.path.join(path, "tokenizer.pkl")):
            raise ValueError(cls.load.__name__ + ": No tokenizer found at the specified directory")
        with open(tokenizer_file, "rb") as pkl_file:
            return pickle.load(pkl_file)
        
    def save(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "tokenizer.pkl"), 'wb') as pkl_file:
            pickle.dump(self, pkl_file)
            
    
    def train(self, corpus_path: str, vocab_size: int) -> None:    
        with open(corpus_path) as f: corpus = f.read()
        ids = torch.tensor(list(corpus.encode('utf-8', errors='replace')), dtype=torch.int16, device=self.device)
        num_merges = max(0, vocab_size - 256)
        self.merges = generate_merges(ids, num_merges)
        for pair, new_idx in self.merges.items():
            self.vocab[new_idx] = self.vocab[pair[0]] + self.vocab[pair[1]]
        self.isTrain = True
        
    def encode(self, string: str) -> torch.Tensor: 
        if self.isTrain == False: print('Warning: Please train the tokenizer first!!!')        
        ids = torch.tensor(list(string.encode("utf-8", errors='replace')), dtype=torch.int16, device=self.device)
        for pair, target in self.merges.items():
            ids = merge_ids(ids, pair, target)
        return ids

    def decode(self, tokens: torch.Tensor) -> str:
        if self.isTrain == False: print('Warning: Please train the tokenizer first!!!')
        string = ""
        for token in tokens:
            string += self.vocab[token.item].decode('utf-8', errors='replace')
        return string
        
        

tok = Tokenizer()
start_time = time.time()
tok.train('/Users/sam/Desktop/github/word2vec/src/sample.txt', 276)
print("\nTraining Finished\n")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds\n")