"""Generate Markov text from text files."""

from random import choice
import sys


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    return open(file_path).read()


def make_chains(text_string):
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

    chains = {}  # created a dictionary

    words = text_string.split()  # split string using any character

    for i in range(
        len(words) - 2
    ):  # create a for loop, iterated through index of list of words (excluding last 2 words to end the loop
        key = (words[i], words[i + 1])
        if key in chains:  # create a key - two first words
            chains[key].append(words[i + 2])
        else:
            chains[key] = [words[i + 2]]
    return chains


def make_text(chains):
    """Return text from chains."""

    words = []

    # Loop through
    # Make a new key out of the second ford from first key, and random word from values.
    first_key = choice(list(chains.keys()))
    word_to_add = choice(chains[first_key])
    words.append(word_to_add)

    key = generate_key(first_key, word_to_add)
    # Loop:
    while key in chains:
        # Lookup key in dict.

        # If exsist
        #   pick random word from values
        word_to_add = choice(chains[key])
        words.append(word_to_add)
        key = generate_key(key, word_to_add)
    #   break. Or check for KeyError?
    # keep doing it.
    #

    return " ".join(words)


def generate_key(previous_key, word):
    next_key = (previous_key[1], word)
    return next_key


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print(random_text)
