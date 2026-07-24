class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

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

    def get_frequency(self, word):
        current = self.root

        for char in word:
            if char not in current.children:
                return -1

            current = current.children[char]

        if current.is_end_of_word:
            return current.frequency

        return -1
    
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
        # Điều kiện dừng
        if errors > max_errors:
            return

        # Trường hợp khi hết input
        if index == len(word):
            if node.is_end_of_word:
                results.append((current_word, errors, node.frequency))
            return

        current_char = word[index]

        # Exact match (khớp bình thường)
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
        
        # Substitution (sai kí tự)
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

        # Insertion (chèn kí tự)
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

        # Deletion (xóa kí tự)
        self._fuzzy_search_recursive(
            node=node,
            word=word,
            index=index + 1,
            errors=errors + 1,
            current_word=current_word,
            max_errors=max_errors,
            results=results
        )