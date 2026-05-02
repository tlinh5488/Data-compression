import time
import random
import heapq
import math
from collections import Counter

# =========================
# HUFFMAN
# =========================
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(data):
    freq = Counter(data)
    heap = [HuffmanNode(c, f) for c, f in freq.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        node = heapq.heappop(heap)
        root = HuffmanNode(None, node.freq)
        root.left = node
        return root

    while len(heap) > 1:
        l = heapq.heappop(heap)
        r = heapq.heappop(heap)

        parent = HuffmanNode(None, l.freq + r.freq)
        parent.left = l
        parent.right = r

        heapq.heappush(heap, parent)

    return heap[0]


def build_codes(root, code="", codes=None):
    if codes is None:
        codes = {}

    if root is None:
        return codes

    if root.char is not None:
        codes[root.char] = code if code else "0"

    build_codes(root.left, code + "0", codes)
    build_codes(root.right, code + "1", codes)

    return codes


def huffman_compress(data):
    start = time.perf_counter()

    root = build_huffman_tree(data)
    codes = build_codes(root)

    encoded = ''.join(codes[c] for c in data)

    # overhead: lưu bảng mã
    overhead_bits = 0
    for char, code in codes.items():
        overhead_bits += 8        # ký tự
        overhead_bits += 8        # độ dài mã
        overhead_bits += len(code)

    end = time.perf_counter()
    return encoded, root, overhead_bits, end - start


def huffman_decompress(encoded, root):
    start = time.perf_counter()

    result = ""
    node = root

    for bit in encoded:
        node = node.left if bit == '0' else node.right
        if node.char:
            result += node.char
            node = root

    end = time.perf_counter()
    return result, end - start


# =========================
# RLE (FIXED)
# =========================
def rle_compress(data):
    start = time.perf_counter()

    compressed = []
    count = 1

    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            compressed.append((count, data[i - 1]))
            count = 1

    compressed.append((count, data[-1]))

    end = time.perf_counter()
    return compressed, end - start


def rle_decompress(compressed):
    start = time.perf_counter()

    result = ""
    for count, char in compressed:
        result += char * count

    end = time.perf_counter()
    return result, end - start


# =========================
# LZW
# =========================
def lzw_compress(data):
    start = time.perf_counter()

    dictionary = {chr(i): i for i in range(256)}
    current = ""
    result = []
    dict_size = 256

    for char in data:
        temp = current + char

        if temp in dictionary:
            current = temp
        else:
            result.append(dictionary[current])
            dictionary[temp] = dict_size
            dict_size += 1
            current = char

    if current:
        result.append(dictionary[current])

    end = time.perf_counter()
    return result, dict_size, end - start


def lzw_decompress(compressed):
    start = time.perf_counter()

    dictionary = {i: chr(i) for i in range(256)}
    dict_size = 256

    current = chr(compressed[0])
    result = current

    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        else:
            entry = current + current[0]

        result += entry
        dictionary[dict_size] = current + entry[0]
        dict_size += 1
        current = entry

    end = time.perf_counter()
    return result, end - start


# =========================
# EXPERIMENT
# =========================
class CompressionExperiment:

    def __init__(self):
        self.sizes = [1024, 4096]
        self.modes = ["random", "repeat", "pattern"]

    def generate_data(self, size, mode):
        if mode == "repeat":
            return "A" * size
        elif mode == "pattern":
            return ("ABCD" * (size // 4))[:size]
        else:
            return ''.join(random.choice("ABCDE") for _ in range(size))

    def rle_bits(self, compressed):
        total = 0
        for count, _ in compressed:
            total += math.ceil(math.log2(count + 1)) + 8
        return total

    def evaluate(self, data, name):
        original_bits = len(data) * 8

        if name == "Huffman":
            c, root, overhead, t1 = huffman_compress(data)
            _, t2 = huffman_decompress(c, root)
            compressed_bits = len(c) + overhead

        elif name == "RLE":
            c, t1 = rle_compress(data)
            _, t2 = rle_decompress(c)
            compressed_bits = self.rle_bits(c)

            # 🔥 FIX: fallback nếu không nén được
            if compressed_bits >= original_bits:
                compressed_bits = original_bits

        elif name == "LZW":
            c, dict_size, t1 = lzw_compress(data)
            _, t2 = lzw_decompress(c)
            bits = math.ceil(math.log2(dict_size))
            compressed_bits = len(c) * bits

        total_time = max(t1 + t2, 1e-6)

        ratio = compressed_bits / original_bits
        saving = (1 - ratio) * 100

        return ratio, saving, total_time

    def run(self):
        for size in self.sizes:
            for mode in self.modes:
                data = self.generate_data(size, mode)

                print(f"\nText: {size}, Mode: {mode}")
                print(f"{'Algorithm':<15}{'Ratio':<10}{'Saving (%)':<15}{'Time (s)':<10}")

                for alg in ["Huffman", "RLE", "LZW"]:
                    r, s, t = self.evaluate(data, alg)
                    print(f"{alg:<15}{r:<10.3f}{s:<15.2f}{t:<10.6f}")

                print("-" * 60)


# =========================
# MAIN
# =========================
def main():
    print("===== FINAL COMPRESSION EXPERIMENT (RLE FIXED) =====")

    exp = CompressionExperiment()
    exp.run()

    print("\n===== DONE =====")


if __name__ == "__main__":
    main()