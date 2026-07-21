"""
Trie Data Structure Implementation for Problem D (C-R-O-S-S-W-O-R-D).

This module provides a memory-optimized Character Trie (Prefix Tree) designed
to load large English vocabularies (>150,000 words) within the strict memory
and Cold Boot performance thresholds (< 2 seconds).

Classes:
    TrieNode: A single node representing a character in the Trie, utilizing
              __slots__ to minimize RAM footprint.
    CharTrie: The main Trie container supporting prefix insertion and
              frequency-based node tracking.
"""

from typing import Dict, Optional


class TrieNode:
    """
    A single node in the Character Trie.

    Architectural Note:
        We use Python's `__slots__` instead of the default dynamic `__dict__`.
        In a vocabulary tree of ~150k+ words (yielding ~800k+ nodes), this
        optimization reduces per-node memory overhead by ~40-50%, keeping total
        RAM usage well below 100MB and preventing memory exhaustion during deep
        wildcard branching.
    """
    __slots__ = ['children', 'is_end_of_word', 'frequency']

    def __init__(self) -> None:
        # Hash map for O(1) child lookups. A dynamic dict is preferred over a
        # static list[26] to prevent memory waste on sparse branches.
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False
        self.frequency: int = 0


class CharTrie:
    """
    Character-level Trie engine responsible for storing words and their
    associated frequency counts for predictive wildcard matching.
    """

    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()

    def insert(self, word: str, frequency: int = 0) -> None:
        """
        Insert a word and its absolute frequency weight into the Trie.

        Args:
            word (str): The target string to insert.
            frequency (int, optional): The usage count of the word from the
                                       corpus. Defaults to 0.

        Time Complexity:
            O(L) where L is the length of the word.
        """
        current_node = self.root
        word = word.lower()

        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]

        current_node.is_end_of_word = True
        current_node.frequency = frequency

    def count_nodes(self, node: Optional[TrieNode] = None) -> int:
        """
        Recursively count total nodes in the Trie. Used primarily for memory
        profiling and Phase 3 validation benchmarks.

        Args:
            node (Optional[TrieNode], optional): The starting node. Defaults
                                                 to self.root.

        Returns:
            int: Total number of TrieNode instances in the subgraph.
        """
        if node is None:
            node = self.root

        count = 1
        for child in node.children.values():
            count += self.count_nodes(child)
        return count