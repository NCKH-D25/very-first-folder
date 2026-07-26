def clean_tokenize (text):
    """
    Remove all symbols, keep only words, and create
    2-gram by using a sliding window.
    """
    text = text.lower()
    delete_symbols = "!@#$%^&*()_+{}|:<>?-=[]\;',./"
    for letter in delete_symbols:
        text = text.replace(letter, "")
    words = text.split()
    data = []
    for i in range (len(words) - 1):
        word_1 = words[i]
        word_2 = words[i+1]
        data.append((word_1, word_2))
    return data

