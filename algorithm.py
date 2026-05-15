import heapq
from collections import Counter
import math

# =====================================================
# HUFFMAN ALGORITHM
# =====================================================
def huffman_compress(text):
    if not text: return "", {}, 0, {}
    freq = Counter(text)
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]: pair[1] = '0' + pair[1]
        for pair in hi[1:]: pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    codes = {pair[0]: pair[1] for pair in heap[0][1:]}
    compressed = "".join(codes[char] for char in text)
    return compressed, codes, len(compressed), freq

def huffman_decompress(compressed_data, codes):
    if not compressed_data or not codes: return ""
    inv_codes = {v: k for k, v in codes.items()}
    result = []
    current_code = ""
    for bit in compressed_data:
        current_code += bit
        if current_code in inv_codes:
            result.append(inv_codes[current_code])
            current_code = ""
    return "".join(result)

# =====================================================
# RLE ALGORITHM
# =====================================================
def rle_compress(text):
    if not text: return [], 0
    res = []
    if len(text) == 0: return res, 0
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i-1]:
            count += 1
        else:
            res.append([count, text[i-1]])
            count = 1
    res.append([count, text[-1]])
    return res, len(res)

def rle_decompress(data):
    res = []
    for count, char in data:
        res.append(char * count)
    final_text = "".join(res)
    return final_text, len(final_text)

# =====================================================
# LZW ALGORITHM
# =====================================================
def lzw_compress(text):
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []
    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result, dict_size, len(result)

def lzw_decompress(compressed):
    if not compressed: return "", 0
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    
    w = chr(compressed[0])
    result = [w]
    for k in compressed[1:]:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError(f"Bad compressed k: {k}")
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return "".join(result), dict_size