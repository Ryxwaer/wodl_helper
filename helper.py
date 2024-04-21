import nltk
from nltk.corpus import wordnet

# Ensure the WordNet data is available
nltk.download('wordnet', quiet=True)

EXCLUDED_WORDS = ["ORINASE", "BELMONT"]

def count_common_letters(word1, word2):
    return len(word1 & word2)

def get_words_of_length(n, words):
    return [word for word in words if len(word) == n]

def get_base_form_words(pos=wordnet.NOUN):
    lemmas = set()
    for synset in wordnet.all_synsets(pos=pos):
        lemmas.update(lemma.name() for lemma in synset.lemmas() if '_' not in lemma.name() and lemma.name() not in EXCLUDED_WORDS)
    return list(lemmas)

def findWords(letters_in, letters_not_in, positions, words):
    letters_in = set(letters_in)
    letters_not_in = set(letters_not_in)
    filtered_words = []

    for word in words:
        if letters_in.issubset(word) and not letters_not_in.intersection(word) and all(
                p == '' or (i < len(word) and word[i] == p) for i, p in enumerate(positions)):
            filtered_words.append(word)

    return filtered_words

def most_likely_word(input_words):
    # Create a set of letters from each word for efficient comparison
    words_sets = {word: set(word) for word in input_words}

    # Calculate the word with the most common letters
    common_letters_count = {word: sum(count_common_letters(letters, other_letters)
                                    for other_word, other_letters in words_sets.items() if other_word != word)
                            for word, letters in words_sets.items()}
    return max(common_letters_count, key=common_letters_count.get)

# Load base form words and convert to uppercase once
base_words = get_base_form_words()
base_words = [word.upper() for word in base_words]

# Configuration
number_of_letters = 7
letters_in = "etn"
letters_not_in = "rsiaelem"
positions = ["", "", "", "", "E", "N", "T"]

# Prepare data
letters_in = set(letters_in.upper())
letters_not_in = set(letters_not_in.upper()) - letters_in
words_of_length = get_words_of_length(number_of_letters, base_words)

if not letters_in and not letters_not_in:
    print("The word with the most letters common with other words is:", most_likely_word(words_of_length))
    exit()

# Find matching words based on the criteria
resulting_words = findWords(letters_in, letters_not_in, positions, words_of_length)
print(resulting_words)

print("The word with the most letters common with other words is:", most_likely_word(resulting_words))