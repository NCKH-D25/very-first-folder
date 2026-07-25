import math

class Trienode:
    def __init__(self):
        self.children = {}
        self.frequency = 0
        self.is_word = False
        self.word = None
class Trie:
    def __init__(self):
        self.root = Trienode()
        
    def insert(self, word: str, frequency: int) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = Trienode()
            node = node.children[char]
        node.is_word = True
        node.word = word
        node.frequency = frequency
        
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word
    
    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
    def get_node(self, prefix: str) -> Trienode:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def collect_words(self, node: Trienode, results: list[(str, int)]):
        if node.is_word:
            results.append((node.word, node.frequency))
        for child in node.children.values():
            self.collect_words(child, results)
            
    def autocomplete(self, prefix: str) -> list[(str, int)]:
        node = self.get_node(prefix)
        if node == None:
            return []
        results = []
        self.collect_words(node, results)
        #print(results)
                    
        results.sort(key = lambda x: -x[1])
        
        #print(results)
        return results

    # algorithm
    def fuzzy_search(self, word: str, max_errors: int = 2,top_k: int = 5):
        candidates = []
        self._fuzzy_search_recursive(node=self.root, word=word, index=0,errors=0,current_word="",max_errors=max_errors,candidates=candidates)

        #Soring Leastest Error and Most Frequency
        candidates.sort(key=lambda item: (item['errors'], -item['frequency']))
        # only get top k results
        return[item['word'] for item in candidates[:top_k]]

    def _fuzzy_search_recursive(self,node: Trienode,word: str,index: int,errors: int,current_word: str,max_errors: int,candidates: list):
        # stop
        if errors > max_errors:
            return

        if index == len(word):
            # if node is end of a word, add to candidates
            if node.is_word:
                candidates.append({"word": node.word,"errors": errors,"frequency": node.frequency})

            # error insertion: add extra characters
            if errors < max_errors:
                for char, child in node.children.items():
                    self._fuzzy_search_recursive(
                        node=child,
                        word=word,
                        index=index,
                        errors=errors + 1,
                        current_word=current_word + char,
                        max_errors=max_errors,
                        candidates=candidates
                    )
            return

        # current input character
        current_char = word[index]

        # same character
        if current_char in node.children:
            self._fuzzy_search_recursive(
                node=node.children[current_char],
                word=word,
                index=index + 1,
                errors=errors,
                current_word=current_word + current_char,
                max_errors=max_errors,
                candidates=candidates
            )
        # over error limit
        if errors >= max_errors:
            return

        # thay ký tự (substitution)
        for char, child in node.children.items():
            if char != current_char:
                self._fuzzy_search_recursive(
                    node=child,
                    word=word,
                    index=index + 1,
                    errors=errors + 1,
                    current_word=current_word + char,
                    max_errors=max_errors,
                    candidates=candidates
                )

        # chèn ký tự (insertion)
        for char, child in node.children.items():
            self._fuzzy_search_recursive(
                node=child,
                word=word,
                index=index,
                errors=errors + 1,
                current_word=current_word + char,
                max_errors=max_errors,
                candidates=candidates
            )
        # xóa ký tự (deletion)
        self._fuzzy_search_recursive(
            node=node,
            word=word,
            index=index + 1,
            errors=errors + 1,
            current_word=current_word,
            max_errors=max_errors,
            candidates=candidates
        )

    # rank candidates based on accuracy and popularity
    def rank_results(self,candidates: list,max_errors: int):
        if not candidates:
            return candidates

        max_frequency = max(candidate["frequency"]
            for candidate in candidates
            )

        if max_frequency == 0:
            max_frequency = 1

        for candidate in candidates:
            errors = candidate["errors"]
            frequency = candidate["frequency"]

            accuracy_score = 1 / (1 + errors)
            popularity_score = (math.log(1 + frequency) / math.log(1 + max_frequency))

        candidates.sort(key=lambda candidate: candidate["errors"])
        return candidates