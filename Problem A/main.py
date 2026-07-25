from preprocess import clean_tokenize
from trie import NGramTree
from predictor import WordPredictor


def load_training_data(filename):
    """
    Read the training corpus from a text file.
    """

    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def main():

    # Read dataset
    raw_text = load_training_data("training_sentences.txt")

    # Preprocess text into 2-grams
    two_grams = clean_tokenize(raw_text)

    # Build Trie
    tree = NGramTree()
    tree.build_from_2grams(two_grams)

    # Start predictor
    predictor = WordPredictor(tree)
    predictor.run()


if __name__ == "__main__":
    main()
