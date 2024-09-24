# BPE tokenizer

## valid utf-8 token Sequences

| **Unicode Index** | **No. of Bytes** | **Byte1** | **Byte2** | **Byte3** | **Byte4** |
|---------------------|---------------------|-----------------|-----------------|-----------------|-----------------|
| 0-127 | 1  | (0-127) |  |  |  |
| 128-2047 | 2 | (192-223) | (128-191) |  |  |
| 2048-65535 | 3 | (192-223) | (128-191) | (128-191) |  |
| Rest | 4 | (240-247) | (128-191) | (128-191) | (128-191) |


- Decimal representation for each byte
- English Characters: 1 token
- Hindi Characters: 3 Tokens
  

