"""
predictor.py

TASK 3 - NEXT WORD PREDICTION TOOL

This module contains all prediction logic.

The Trie only stores the training data.
Searching, ranking, predicting, and displaying
results are handled in this module.
"""

from trie import TrieNode


class WordPredictor:
    def __init__(self, tree, top_k=5):
        """
        Initialize the prediction engine.

        Parameters
        ----------
        tree : NGramTree
            Trie built from the training dataset.

        top_k : int
            Maximum number of predictions to display.
        """
        self.tree = tree
        self.top_k = top_k

    def search_node(self, word):
        """
        Search for a node matching the input word.

        If the word does not exist, create a new
        branch from the root and return it.
        """

        node = self.tree.root.children.get(word)

        if node is None:
            node = TrieNode(word)
            node.frequency = 1
            self.tree.root.children[word] = node

        return node

    def get_candidates(self, node):
        """
        Retrieve all possible next words.

        Returns
        -------
        list
            A list of tuples in the format:
            (next_word, frequency)
        """

        candidates = []

        for word, child in node.children.items():
            candidates.append((word, child.frequency))

        return candidates

    def sort_candidates(self, candidates):
        """
        Sort prediction candidates by:

        1. Frequency (descending)
        2. Alphabetical order (ascending)
        """

        return sorted(
            candidates,
            key=lambda item: (-item[1], item[0])
        )

    def predict(self, word):
        """
        Return the Top-K predicted next words.
        """

        node = self.search_node(word)

        candidates = self.get_candidates(node)

        if not candidates:
            return []

        ranked = self.sort_candidates(candidates)

        return ranked[:self.top_k]

    def display_prediction(self, word):
        """
        Display prediction results.
        """

        predictions = self.predict(word)

        print(f"\nInput: {word}")

        if not predictions:
            print("No prediction found, new node created.")
            return

        print("\nTop 5 Predictions\n")

        for index, (next_word, frequency) in enumerate(predictions, start=1):
            print(f"{index}. {next_word:<20} ({frequency})")

    def run(self):
        """
        Start the prediction tool.

        The program continues running until
        the user presses Enter twice consecutively.
        """

        empty_count = 0
        input_history = []

        print("NEXT WORD PREDICTOR")  

        while True:

            word = input("\nEnter a word: ").strip().lower()

            if word == "":

                empty_count += 1

                if empty_count == 2:

                    print("\n INPUT HISTORY ")

                    if input_history:
                        print("Input sequence:")
                        print(" ".join(input_history))
                    else:
                        print("No words were entered.")

                    print("\nProgram terminated.")
                    break

                continue

            empty_count = 0

            input_history.append(word)

            self.display_prediction(word)
