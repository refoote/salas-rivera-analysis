from curses import raw
import nltk
from nltk.corpus import stopwords
from numpy import append
# get your data 
filename = "antes_linebreak.txt"
with open(filename, 'r') as fin:
    raw_text = fin.read()

#look another test

# do something with it
num_characters = len(raw_text)
# split that long string on spaces
split_tokens = raw_text.split()
raw_tokens = nltk.word_tokenize(raw_text)
unique_words = set(raw_tokens)
fd = nltk.FreqDist(raw_tokens)

bigrams = list(nltk.bigrams(raw_tokens))
most_common_bigrams = nltk.FreqDist(list(nltk.bigrams(raw_tokens)))

# show those results
print("number of characters: " + str(len(raw_text)))
print("number of words split by spaces: " + str(len(split_tokens)))
print("number of words split by nltk's tokenizer: " + str(len(raw_tokens)))
print("num of unique words: " + str(len(unique_words)))

nltk_text = nltk.Text(raw_tokens)

def import_poem(filename):
    filename = "antes.txt"
    with open(filename, 'r') as fin:
        raw_text = fin.read()
    return raw_text

def convert_raw_text_to_poems(raw_text):
    """Take the raw_text and break it into poems"""
    return raw_text.split('\n\n\n\n')

def convert_poems_into_stanzas(list_of_poems):
    poems_as_stanzas = [poem.split('\n\n\n') for poem in list_of_poems]
    return poems_as_stanzas

def convert_stanzas_into_lines(poems_as_stanzas):
    lines = [stanza.split('\n\n') for stanzas in poems_as_stanzas for stanza in stanzas]
    return lines


def line_midpoint(line):
    """takes a line and divides it in half"""
    line_as_tokens = nltk.word_tokenize(line)
    length_of_line = len(line_as_tokens)
    half = int(length_of_line / 2)
    first_half = line_as_tokens[:half]
    second_half = line_as_tokens[half:]

    return (first_half, second_half)

def find_chiasmus_in_line_using_simple_token_matching(two_halves):
    """Take two halves. Look to see if a token exists in each half. If so, return true."""
    first_half = two_halves[0]
    second_half = two_halves[1]
    stopwords_list = stopwords.words('english')

    stopped_first_half = [word for word in first_half if word not in stopwords_list]
    stopped_second_half = [word for word in second_half if word not in stopwords_list]
    return bool(set(stopped_first_half) & set(stopped_second_half))

def find_chiasmus_over_whole_collection(raw_text):
    """Take in a raw text. Split it into lines-ish. And print out every line-ish that has chiasmus in it."""
    raw_text = import_poem('antes.txt')
    raw_lines_ish = raw_text.split('\n')
    results = []
    for line in raw_lines_ish:
        line_halves = line_midpoint(line)
        if find_chiasmus_in_line_using_simple_token_matching(line_halves):
            print('=========')
            print(line_halves)
            print(line)
            results.append((line,line_halves))
    return results

# TODO: Elise - annotate the code in your own words - again.
# TODO: Elise - practice using it by importing it in the terminal.
# TODO: Elise - maybe try to make a new function that does a thing.
# TODO: Brandon - find a better way to turn the file into lines of poetry
# TODO: Brandon - Double check why the chiasmus printing function isn't working

# TO USE
# in the same folder, open the interpreter.
# $ python3
# >>>
# three less than signs shows you're in the interpreter.
# import your file using the import method
# >>> import analysis
# The functions you write will be under analysis - 
# raw_text = analysis.import_poem('antes.txt')
# >>> chiasmus = find_chiasmus_over_whole_collection(raw_text)
# if you change something, the terminal won't know about it. so you will need to reimport the library using importlib like so-
# import importlib
# importlib.reload(analysis)
# you'll then need to remake any variables that might have changed
# line_halves = analysis.line_midpoint(line)

# to run the chiasmus function:
# import analysis
# raw_text = analysis.import_poem('antes.txt')
# results = analysis.find_chiasmus_over_whole_collection(raw_text)
# for result in results:
#   print('=======')
#   print(result)