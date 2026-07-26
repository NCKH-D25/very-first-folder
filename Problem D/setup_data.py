"""
Master Vocabulary Builder and Frequency Blending Pipeline for Problem D.

This tool merges dwyl's 370,000-word comprehensive English dictionary with
Dr. Peter Norvig's Google Web Trillion Word Corpus frequency data (~333k words).
Rare valid words lacking corpus data are assigned a realistic low baseline
frequency (5-50) to preserve total lexical recall without disrupting UX ranking.
"""

import urllib.request
import random
import time
import sys
from typing import Dict, Set


def fetch_master_vocabulary() -> Set[str]:
    """Fetch the complete 370k English word list (dwyl/english-words)."""
    url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    print("[1/3] Downloading master English vocabulary (~370,000 words)...")
    
    # Thêm User-Agent chuẩn để tránh bị GitHub tường lửa chặn
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    request = urllib.request.Request(url, headers=req_headers)
    
    with urllib.request.urlopen(request, timeout=20) as response:
        words = {line.decode('utf-8').strip().lower() for line in response}
        
    print(f"      -> Loaded {len(words):,} valid dictionary words.")
    return words


def fetch_norvig_frequencies(valid_vocab: Set[str]) -> Dict[str, int]:
    """Fetch Peter Norvig's Google Web Trillion Word frequency corpus (~333k words)."""
    url = "https://norvig.com/ngrams/count_1w.txt"
    print("[2/3] Downloading Dr. Peter Norvig's Google Web Corpus frequencies...")
    
    req_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    request = urllib.request.Request(url, headers=req_headers)
    
    freq_map: Dict[str, int] = {}
    print("      -> Cross-referencing Google Ngrams with master vocabulary...")
    
    with urllib.request.urlopen(request, timeout=25) as response:
        for line in response:
            parts = line.decode('utf-8').strip().split()
            if len(parts) >= 2:
                word = parts[0].lower()
                # Chỉ lấy những từ hợp lệ có trong từ điển chuẩn 370k
                if word in valid_vocab and (len(word) > 1 or word in ('a', 'i')):
                    try:
                        freq_map[word] = int(parts[1])
                    except ValueError:
                        continue
                
    print(f"      -> Mapped real-world Google counts for {len(freq_map):,} words.")
    return freq_map


def build_hyper_dataset(output_filepath: str = "dataset.txt") -> None:
    """Execute the blending pipeline to generate the final master dataset."""
    print("=" * 60)
    print("      INITIALIZING HYPER-COMPREHENSIVE DATASET PIPELINE      ")
    print("=" * 60)
    start_time = time.perf_counter()

    try:
        valid_vocab = fetch_master_vocabulary()
        freq_map = fetch_norvig_frequencies(valid_vocab)

        print("[3/3] Blending datasets and assigning baseline counts to rare words...")
        final_entries = []
        random.seed(42)  # Deterministic random baseline for reproducible builds

        for word in valid_vocab:
            if len(word) <= 1 and word not in ('a', 'i'):
                continue
            
            if word in freq_map:
                # Từ có trong kho Google -> Dùng count thực tế (khổng lồ)
                final_entries.append((word, freq_map[word]))
            else:
                # Từ cổ/chuyên ngành siêu hiếm -> Gán count nền nhỏ (5-50)
                baseline_count = random.randint(5, 50)
                final_entries.append((word, baseline_count))

        print("      -> Sorting 370,000+ words by frequency descending...")
        final_entries.sort(key=lambda x: (-x[1], x[0]))

        print(f"[*] Writing master dataset to '{output_filepath}'...")
        with open(output_filepath, "w", encoding="utf-8") as file:
            for word, count in final_entries:
                file.write(f"{word},{count}\n")

        elapsed = time.perf_counter() - start_time
        print("-" * 60)
        print(f"[+] SUCCESS: Master dataset '{output_filepath}' generated!")
        print(f"[+] Total Vocabulary Size : {len(final_entries):,} words")
        print(f"[+] Total Execution Time  : {elapsed:.2f} seconds")
        print("=" * 60)
        print("[!] Run 'python main.py' to load the full 370k dictionary into RAM!")

    except Exception as e:
        print(f"\n[!] CRITICAL ERROR during pipeline execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    build_hyper_dataset()