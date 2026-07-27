from predict import Skill


class TrieNode:
    def __init__(self):
        self.children: dict[Skill, "TrieNode"] = {}
        self.frequency: int = 0


class NGramTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, sequence: list[Skill]) -> None:
        if not sequence:
            return

        node = self.root
        for skill in sequence:
            if skill not in node.children:
                node.children[skill] = TrieNode()
            node = node.children[skill]

        node.frequency += 1

    def search(self, context: list[Skill]) -> dict[Skill, int]:
        node = self.root
        for skill in context:
            if skill not in node.children:
                return {}
            node = node.children[skill]

        result = {}
        for next_skill, child_node in node.children.items():
            result[next_skill] = child_node.frequency

        return result
