class TrieNode:
    def __init__(self):
        self.children = {}
        self.frequency = 0
class NGramTree:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, sequence):
        current_node = self.root
        for word in sequence:
            if word not in current_node.children:
                current_node.children[word] = TrieNode()
            current_node = current_node.children[word]
        current_node.frequency += 1
    def build_from_2grams(self, two_grams_list):
        for gram in two_grams_list:
            self.insert(gram)