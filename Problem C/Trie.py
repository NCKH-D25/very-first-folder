class TrieNode:
    def __init__(self):
        self.children = {} 
        self.is_end_of_word = False 
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def __init__(self, error_weight, frequency_weight):
        self.root = TrieNode()

        self.error_weight = error_weight
        self.frequency_weight = frequency_weight

    def insert(self, word, frequency=0):
        current = self.root

        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()

            current = current.children[char]

        current.is_end_of_word = True
        current.frequency = frequency

    def search(self, word):
        current = self.root

        for char in word:
            if char not in current.children:
                return False
    
            current = current.children[char]

        return current.is_end_of_word
    def _find_node(self, word):
        current = self.root

        for char in word:
            if char not in current.children:
                return None

        current = current.children[char]

        return current
    
    def get_frequency(self, word):
        node = self._find_node(word)

        if node is None or not node.is_end_of_word:
            return None

        return node.frequency
    
    def predict_fuzzy(self, word, max_errors=1):
        results = []
    
        self._fuzzy_search_recursive(
            node=self.root,
            word=word,
            index=0,
            errors=0,
            current_word="",
            max_errors=max_errors,
            results=results
        )
    
        return results

    def _fuzzy_search_recursive(self, node, word, index, errors, current_word, max_errors, results):
        # Dieu kien dung
        if errors > max_errors:
            return

        # Truong hop khi doc het input
        if index == len(word):
            if node.is_end_of_word:
                results.append((current_word, errors, node.frequency))
            return

        current_char = word[index]

        # Exact match
        if current_char in node.children:
            self._fuzzy_search_recursive(
                node=node.children[current_char],
                word=word,
                index=index + 1,
                errors=errors,
                current_word=current_word + current_char,
                max_errors=max_errors,
                results=results
            )
        
        if errors >= max_errors:
            return
        
        # Substitution (sai ki tu)
        for char, child in node.children.items():
            if char != current_char:
                self._fuzzy_search_recursive(
                    node=child,
                    word=word,
                    index=index + 1,
                    errors=errors + 1,
                    current_word=current_word + char,
                    max_errors=max_errors,
                    results=results
                )

        # Insertion (chen ki tu)
        for char, child in node.children.items():
            self._fuzzy_search_recursive(
                node=child,
                word=word,
                index=index,
                errors=errors + 1,
                current_word=current_word + char,
                max_errors=max_errors,
                results=results
            )

        # Deletion (xoa ki tu)
        self._fuzzy_search_recursive(
            node=node,
            word=word,
            index=index + 1,
            errors=errors + 1,
            current_word=current_word,
            max_errors=max_errors,
            results=results
        )