# BPE tokenizer

This README describes a GPT-2 style tokenizer implemented using the Byte Pair Encoding (BPE) algorithm. The tokenizer is designed to handle UTF-8 encoded text, with specific considerations for various Unicode ranges.

---
### Valid utf-8 token Sequences

| **Unicode Index** | **No. of Bytes** | **Byte1** | **Byte2** | **Byte3** | **Byte4** |
|---------------------|---------------------|-----------------|-----------------|-----------------|-----------------|
| 0-127 | 1  | (0-127) |  |  |  |
| 128-2047 | 2 | (192-223) | (128-191) |  |  |
| 2048-65535 | 3 | (192-223) | (128-191) | (128-191) |  |
| Rest | 4 | (240-247) | (128-191) | (128-191) | (128-191) |


- Decimal representation for each byte
- English Characters: 1 token
- Hindi Characters: 3 Tokens
---


### Usage

1. Initialise variables in paths.py<br>
    DIRECTORY: /path/to/main/directory<br>
    SOURCE: /source/folder/containing/all/files

**Note**: The specified directory can include .txt files or subdirectories, they will be processed accordingly.


2. The tokenizer trains on raw .txt files. Run the following command in corpus.py to generate training corpus

```
generate_corpus(DIRECTORY)
```


3. To train the tokenizer of required vocabulary size 
```
tok = Tokenizer()
tok.train(SOURCE, Vocab_size)
```
---


