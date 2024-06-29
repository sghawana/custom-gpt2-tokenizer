import pickle

def get_token_pair_counts(tokens_list: list[int]) -> dict[tuple[int, int], int]:
    token_pair_counts = {}
    for i in range(1,len(tokens_list)):
        pair = (tokens_list[i-1],tokens_list[i])
        if pair in token_pair_counts:
            token_pair_counts[pair] += 1
        else:
            token_pair_counts[pair] = 1
    return token_pair_counts


def merge_tokens(tokens_list: list[int], pair: tuple[int, int], new_token: int) -> list[int]:
    i = 1
    while i < len(tokens_list):
        if (tokens_list[i-1], tokens_list[i]) == pair:
            tokens_list[i-1] = new_token
            tokens_list.pop(i)
        else:
            i += 1
    return tokens_list

def unmerge_tokens(tokens_list: list[int], pair: tuple[int, int], new_token: int) -> list[int]:
    ...



def generate_merges(tokens_list: list[int], num_merges: int) -> dict[tuple[int, int], int]:
    merges = {}
    i = 256
    count = 0
    while count < num_merges:
        pair_count = get_token_pair_counts(tokens_list)
        merge_pair = sorted(pair_count.items(), reverse=True, key= lambda item : item[1])[0][0]        
        merge_tokens(tokens_list, merge_pair, i)
        merges[merge_pair] = i
        i += 1
        count += 1
    return merges
        
        
def build_vocab(corpus_path, num_merges, destination):
    
    with open(corpus_path) as f: sample_text = f.read()
    tokens_list = list(sample_text.encode('utf-8', errors='replace'))
    
    vocab = {token:i for i,token in enumerate(list(set(tokens_list)))}
    merges = generate_merges(tokens_list, num_merges)
    
    new_tokens = list(merges.values())
    m = len(vocab)
    for token in new_tokens:
        vocab[token] = m
        m += 1
        
    file_name = 'vocab.pkl'
    with open(destination, 'wb') as pkl_file:
        pickle.dump(vocab, pkl_file)
        
    file_name = 'merges.pkl'
    with open(destination, 'wb') as pkl_file:
        pickle.dump(merges, pkl_file)