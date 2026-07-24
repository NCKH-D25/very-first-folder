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