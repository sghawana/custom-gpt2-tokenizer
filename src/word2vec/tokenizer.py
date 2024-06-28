import os

from paths import DATASET_DIRECTORY, SOURCE
from corpus import generate_corpus

from vocab import build_vocab
from corpus import generate_corpus

CORPUS_NAME = 'text_corpus.txt'
NUM_MERGES = 50

corpus_destination = os.path.join(SOURCE, CORPUS_NAME)
generate_corpus(corpus_destination, CORPUS_NAME)
build_vocab(corpus_destination, NUM_MERGES,SOURCE)


    
    
