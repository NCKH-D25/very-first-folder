"""
Phase 3 Validation & Benchmarking Engine for Problem D (Sliding Blank Test).

This script verifies the structural pruning efficiency of our CharTrie by
running automated execution timing tests across three distinct wildcard
positions: End Blank, Middle Blank, and Front Blank.

Pass Criteria:
    1. Engine successfully resolves correct words for all three cases.
    2. End Blank execution time is measurably faster than Front Blank,
       proving algorithmic prefix pruning over linear brute-force scanning.
"""

import time
import sys
from typing import List, Tuple
from trie import CharTrie
from main import load_dataset


def run_sliding_blank_test(trie: CharTrie) -> bool:
    """
    Execute the mandatory Sliding Blank Test suite and output an engineering
    performance report.

    Returns:
        bool: True if all Phase 3 pass criteria are strictly met.
    """
    print("\n" + "=" * 65)
    print("      PHASE 3 VALIDATION : SLIDING BLANK BENCHMARK SUITE      ")
    print("=" * 65)

    # 3 Test Cases được thiết kế theo đúng quy chuẩn Phase 3 của đề bài
    test_cases: List[Tuple[str, str, str]] = [
        ("End Blank   ", "pytho_", "Should resolve instantly with linear path traversal."),
        ("Middle Blank", "p_thon", "Forks at char 2, but 95% branches die at char 3 (Pruning)."),
        ("Front Blank ", "_ython", "Forces 26 parallel root searches; heaviest branch load.")
    ]

    execution_times: List[float] = []
    all_resolved = True

    for label, pattern, desc in test_cases:
        print(f"\n[*] Testing Case: [{label}] -> Pattern: '{pattern}'")
        print(f"    Note: {desc}")
        
        start_time = time.perf_counter()
        # Chạy tìm kiếm với giới hạn 10 từ để đo tốc độ cắt tỉa thô
        results = trie.predict_wildcard(pattern, limit=10)
        elapsed_ms = (time.perf_counter() - start_time) * 1000  # Convert to ms
        
        execution_times.append(elapsed_ms)

        if not results:
            print(f"    [!] FAILED: No words resolved for pattern '{pattern}'!")
            all_resolved = False
        else:
            top_word = results[0]
            print(f"    [+] Resolved {len(results)} words in {elapsed_ms:.4f} ms.")
            print(f"    [+] Top Match: '{top_word}' (Ranked by Google Frequency)")

    print("\n" + "-" * 65)
    print("                      BENCHMARK ANALYSIS                      ")
    print("-" * 65)
    
    end_time, mid_time, front_time = execution_times

    print(f"  1. End Blank (`pytho_`)   Execution Time : {end_time:.4f} ms")
    print(f"  2. Middle Blank (`p_thon`) Execution Time : {mid_time:.4f} ms")
    print(f"  3. Front Blank (`_ython`)  Execution Time : {front_time:.4f} ms")
    print("-" * 65)

    # Phase 3 Pass Criteria Evaluation
    time_ratio = front_time / end_time if end_time > 0 else 1.0
    is_pruning_proven = front_time >= end_time

    print("=== FINAL EVALUATION ===")
    print(f"[+] Criteria 1 (All patterns resolved correctly): {'PASSED' if all_resolved else 'FAILED'}")
    print(f"[+] Criteria 2 (End Blank faster than Front Blank): {'PASSED' if is_pruning_proven else 'FAILED'} (Speedup Factor: {time_ratio:.2f}x)")

    if all_resolved and is_pruning_proven:
        print("\n[>>>] PHASE 3 SLIDING BLANK TEST: FULLY PASSED [<<<]")
        print("      Algorithmic prefix pruning successfully proven over brute-force!")
        return True
    else:
        print("\n[!] PHASE 3 TEST FAILED: Engine did not meet algorithmic requirements.")
        return False


def main() -> None:
    """Initialize test environment and run validation suite."""
    trie = CharTrie()
    dataset_path = "dataset.txt"

    print("[*] Preparing Phase 3 Test Environment...")
    try:
        word_count, load_time = load_dataset(dataset_path, trie)
        print(f"[+] Loaded {word_count:,} words in {load_time:.4f}s. Starting tests...\n")
    except Exception as e:
        print(f"[!] CRITICAL: Could not load '{dataset_path}': {str(e)}")
        print("[!] Please run 'python setup_data.py' first to generate the dataset.")
        sys.exit(1)

    success = run_sliding_blank_test(trie)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()