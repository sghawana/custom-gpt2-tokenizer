import torch
import heapq

def merge_tokens(tokens: torch.Tensor, pair: tuple[int, int], new_token: int) -> torch.Tensor:

    pair_mask = (tokens[:-1] == pair[0]) & (tokens[1:] == pair[1])
    num_pairs = pair_mask.sum().item()
    new_tokens = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) - 1 and (tokens[i].item(), tokens[i + 1].item()) == pair:
            new_tokens.append(new_token)
            i += 2 
        else:
            new_tokens.append(tokens[i].item())
            i += 1
    return torch.tensor(new_tokens, dtype=tokens.dtype, device=tokens.device)


def unmerge_tokens(tokens: torch.Tensor, pair: tuple[int, int], new_token: int) -> torch.Tensor:
    
    pair_tensor = torch.tensor(pair, dtype=tokens.dtype, device=tokens.device)
    mask = tokens == new_token
    num_pairs = mask.sum().item()
    
    expanded_tokens = torch.empty(tokens.size(0) + num_pairs, dtype=tokens.dtype, device=tokens.device)
    expanded_tokens_index = 0
    for i in range(tokens.size(0)):
        if mask[i]:
            expanded_tokens[expanded_tokens_index] = pair_tensor[0]
            expanded_tokens[expanded_tokens_index + 1] = pair_tensor[1]
            expanded_tokens_index += 2
        else:
            expanded_tokens[expanded_tokens_index] = tokens[i]
            expanded_tokens_index += 1
    
    return expanded_tokens


def get_token_pair_counts(tokens: torch.Tensor) -> dict[tuple[int, int], int]:
    pairs = torch.stack((tokens[:-1], tokens[1:]), dim=1)
    pairs_tuple = [tuple(pair.tolist()) for pair in pairs]
    
    token_pair_counts = {}
    for pair in pairs_tuple:
        if pair in token_pair_counts:
            token_pair_counts[pair] += 1
        else:
            token_pair_counts[pair] = 1

    return token_pair_counts

def generate_merges(tokens: torch.Tensor, num_merges: int) -> dict[tuple[int, int], int]:
    merges = {}
    i = 256
    count = 0
    pair_count = get_token_pair_counts(tokens)
    max_heap = [(-count, pair) for pair, count in pair_count.items()]
    heapq.heapify(max_heap)
    
    while count < num_merges and max_heap:
        neg_count, merge_pair = heapq.heappop(max_heap)
        merge_pair = tuple(merge_pair)
        tokens = merge_tokens(tokens, merge_pair, i)
        merges[merge_pair] = i
        i += 1
        count += 1
        pair_count = get_token_pair_counts(tokens)
        max_heap = [(-count, pair) for pair, count in pair_count.items()]
        heapq.heapify(max_heap)
    
    return merges