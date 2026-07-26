"""
Main Entry Point and CLI Engine for Problem D (C-R-O-S-S-W-O-R-D).

This module handles robust File I/O to load the external vocabulary dataset
into memory, benchmarks Cold Boot execution time to ensure Phase 3 compliance
(< 2 seconds), and runs the interactive terminal loop for wildcard matching.
"""

import sys
import time
from typing import Tuple
from trie import CharTrie


def load_dataset(filepath: str, trie: CharTrie) -> Tuple[int, float]:
    """
    Load vocabulary and frequency weights from an external text file into RAM.

    Architectural Note (Cold Boot Optimization):
        Utilizes time.perf_counter() for high-precision benchmarking. To meet
        the strict Phase 3 threshold (< 2.0 seconds for >50k words), we parse
        lines using lightweight string splitting without regex overhead.

    Args:
        filepath (str): Path to the dataset file (format: word,count).
        trie (CharTrie): The Trie container instance to populate.

    Returns:
        Tuple[int, float]: Total number of valid words loaded, and total
                           elapsed loading time in seconds.

    Raises:
        SystemExit: If the specified file cannot be found or read.
    """
    print(f"[*] Initializing Cold Boot sequence...")
    print(f"[*] Loading vocabulary from '{filepath}' into RAM...")
    
    start_time = time.perf_counter()
    loaded_words = 0

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or "," not in line:
                    continue
                
                try:
                    word, count_str = line.split(",", 1)
                    word = word.strip().lower()
                    frequency = int(count_str.strip())
                    
                    # Ignore single-character noise unless valid 'a' or 'i'
                    if len(word) > 1 or word in ('a', 'i'):
                        trie.insert(word, frequency)
                        loaded_words += 1
                except ValueError:
                    # Skip malformed lines silently during high-speed boot
                    continue

    except FileNotFoundError:
        print(f"\n[!] CRITICAL ERROR: Dataset file '{filepath}' not found.")
        print("[!] Please run the dataset curation script or verify the file path.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] CRITICAL ERROR: Failed to read dataset: {str(e)}")
        sys.exit(1)

    elapsed_time = time.perf_counter() - start_time
    return loaded_words, elapsed_time


def run_cli(trie: CharTrie) -> None:
    """
    Execute the interactive command-line interface (CLI) loop.

    Handles user inputs, triggers wildcard predictions, and formats output
    results according to Phase 2 frequency ranking decisions.
    """
    print("\n" + "=" * 60)
    print("      C-R-O-S-S-W-O-R-D : WILDCARD SEARCH ENGINE      ")
    print("=" * 60)
    print("Instructions:")
    print("  - Use '_' or '?' as single-character wildcards (e.g., 'p_th_n').")
    print("  - Type 'exit' or 'quit' to terminate the program.")
    print("-" * 60)

    while True:
        try:
            query = input("\n[?] Enter search pattern > ").strip().lower()

            if not query:
                continue
            
            if query in ("exit", "quit"):
                print("\n[*] Shutting down engine. Goodbye!")
                break

            start_search = time.perf_counter()
            results = trie.predict_wildcard(query, limit=15)
            search_time = (time.perf_counter() - start_search) * 1000  # in ms

            print(f"\n[*] Results for '{query}' (Found {len(results)} | Time: {search_time:.2f} ms):")
            
            if not results:
                print("    No matching words found in vocabulary.")
            else:
                for rank, word in enumerate(results, 1):
                    print(f"    {rank:2d}. {word}")

        except KeyboardInterrupt:
            print("\n\n[*] Process interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n[!] Error during search: {str(e)}")


def main() -> None:
    """Main program entry point orchestrating setup and execution flow."""
    trie = CharTrie()
    dataset_path = "dataset.txt"

    # Step 1: Load data & verify Cold Boot Phase 3 requirement
    word_count, load_time = load_dataset(dataset_path, trie)
    
    print(f"[+] Successfully loaded {word_count:,} words into Trie.")
    print(f"[+] Cold Boot Execution Time: {load_time:.4f} seconds")

    if load_time > 2.0:
        print("[!] WARNING: Cold Boot time exceeded the 2.0s Phase 3 threshold!")
    else:
        print("[+] Phase 3 Cold Boot Benchmark: PASSED (< 2.0s)")

    # Step 2: Enter interactive user loop
    run_cli(trie)


if __name__ == "__main__":
    main()