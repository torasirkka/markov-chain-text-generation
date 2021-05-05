"""Generate Markov text from text files."""

from random import choice
from typing import Dict, Set, List, Tuple
import sys


def open_and_read_file(file_path: str) -> str:
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    return open(file_path).read()


def make_chains(text_string: str) -> Tuple[Dict[Set[str], List[str]]]:
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}  # instantiate a dictionary to store the chains

    words = text_string.split()  # split string on any punctuation.

    # Create a set of all words that start a sentence (aka are capitalized).
    sentence_starting_words = {word for word in words if word[0].isupper()}

    # Loop through the words list & create new keys and/or add
    # new words to a key value
    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        if key in chains:
            chains[key].append(words[i + 2])
        else:
            chains[key] = [words[i + 2]]
    return (chains, sentence_starting_words)


def make_text(chains: Dict[tuple, List[str]], first_words: Set[str]):
    """Return text from chains and a set of words that
    start sentences in the corpus.

    We keep drawing a starting key and word at random, until an upper case word is found to start our sentence."""

    words = []

    # We instantiate first word and then keep drawing a new one until an uppercase one is found.
    first_word = ""
    while first_word not in first_words:
        first_key = choice(list(chains.keys()))
        first_word = choice(chains[first_key])
    words.append(first_word)

    # The rest of the keys are generated based on the first key
    key = generate_key(first_key, first_word)

    # As long as we choose a key (word sequence) that is seen
    # in the corpus and thereby registered in the chains dict,
    # we will keep building our text (list of words).
    while key in chains:
        word_to_add = choice(chains[key])
        words.append(word_to_add)
        key = generate_key(key, word_to_add)

    # Return one long string by joining all words with a whitespace
    return " ".join(words)


def generate_key(previous_key, word):
    next_key = (previous_key[1], word)
    return next_key


def run_program() -> str:
    input_path = sys.argv[1]

    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)

    # Get a Markov chain
    chains, first_words = make_chains(input_text)

    # Produce random text
    random_text = make_text(chains, first_words)

    return random_text


text = run_program()
print(text)
