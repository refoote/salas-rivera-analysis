from curses import raw
import nltk
# get your data 
filename = "antes.txt"
with open(filename, 'r') as fin:
    raw_text = fin.read()

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

def find_chiasmus(text):
    pass

# TODO: annotate the code in your own words
# TODO: take an example of chiasmus and try to write out how you would define it. in computer terms
# for example - end of sentence (or line). look x number of words before and after and see if they share a term in both places.
# TODO: for next time, we will take one of those definitions and code it together as a function. 