class Trienode:
    def __init__(self):
        self.children = {}
        self.frequency = 0
        self.is_word = False
        self.word = None
class Trie:
    def __init__(self):
        self.root = Trienode()
    def insert(self, word, frequency):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = Trienode()
            node = node.children[char]
        node.is_word = True
        node.word = word
        node.frequency = frequency
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_word
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    def get_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    def collect_words(self, node, results):
        if node.is_word:
            results.append((node.word, node.frequency))
        for child in node.children.values():
            self.collect_words(child, results)
    def autocomplete(self, prefix):
        node = self.get_node(prefix)
        if node == None:
            return []
        results = []
        self.collect_words(node, results)
        #print(results)

        for i in range(len(results)-1):
            for j in range(i+1, len(results)):
                if results[i][1] < results[j][1]:
                    results[i], results[j] = results[j], results[i]
        #print(results)
        return results
