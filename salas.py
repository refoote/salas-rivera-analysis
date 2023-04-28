import nltk
from nltk.corpus import stopwords
import string

class PoetryCollection(object):
    # now create the blueprint for our text object
    def __init__(self, fn='antes_linebreak.txt'):
        # given a filename, store it
        self.filename = fn
        self.raw_collection = self.import_collection()
        self.poems = self.convert_raw_text_to_poems()
        # self.chiasmus_poems = ???? # for next time with Elise

    def import_collection(self):
        with open(self.filename, 'r') as fin:
            raw_text = fin.read()
        return raw_text

    def convert_raw_text_to_poems(self):
        """Take the raw_text and break it into poems"""
        poems = []
        for poem_text in self.raw_collection.split('\n\n\n\n'):
            poems.append(Poem(poem_text))
        return poems    

    def find_chiasmus_over_whole_collection(self):
        for poem in self.poems:
            if poem.has_chiasmus:
                print('=========')
                print(poem.title)
                print(poem.chiasmus_lines)

class Poem(object):
    """a poem blueprint"""
    def __init__(self, raw_text):
        # what do we want the poem to have?
        # list it out
        self.raw_text = raw_text
        punct = string.punctuation +'’'
        self.raw_text_without_punctuation = ('').join([word for word in self.raw_text if word not in punct])
        self.raw_stanzas = self.convert_poems_into_raw_stanzas()
        self.title = self.raw_stanzas[0]
        self.text = (' ').join(self.raw_stanzas[1:])
        #self.text_without_stopwords
        self.stanzas = [stanza.split('\n\n') for stanza in self.raw_stanzas[1:]]
        self.lines = [item for sublist in self.stanzas for item in sublist]
        self.chiasmus_lines = self.find_chiasmus_in_poem()
        if len(self.chiasmus_lines) > 0:
            self.has_chiasmus = True
        else:
            self.has_chiasmus = False


    def convert_poems_into_raw_stanzas(self):
        """Take a poem and split it into stanzas"""
        # this version keeps in punctuation
        # return self.raw_text.split('\n\n\n')
        return self.raw_text_without_punctuation.split('\n\n\n')
    
    def process_raw_stanzas(self, stanzas):
        lines = [stanza.split('\n\n') for stanza in self.stanzas]
        return lines

    def line_midpoint(self, line):
        """takes a line and divides it in half"""
        line_as_tokens = nltk.word_tokenize(line)
        length_of_line = len(line_as_tokens)
        half = int(length_of_line / 2)
        first_half = line_as_tokens[:half]
        second_half = line_as_tokens[half:]
        return (first_half, second_half)

    def find_chiasmus_in_line_using_simple_token_matching(self, two_halves):
        """Take two halves. Look to see if a token exists in each half. If so, return true."""
        first_half = two_halves[0]
        second_half = two_halves[1]
        stopwords_list = stopwords.words('english')

        stopped_first_half = [word for word in first_half if word not in stopwords_list]
        stopped_second_half = [word for word in second_half if word not in stopwords_list]
        return bool(set(stopped_first_half) & set(stopped_second_half))

    def find_chiasmus_in_poem(self):
        results = []
        for line in self.lines:
            line_halves = self.line_midpoint(line)
            if self.find_chiasmus_in_line_using_simple_token_matching(line_halves):
                results.append(line)
                print(line)
                # results.append((line,line_halves))
        return results

# >>> import salas
# >>> collection = salas.PoetryCollection('antes.txt')
# >>> collection.poems
# >>> collection.poems[0].find_chiasmus_in_poem()

# TODO Elise: keep annotating this new monstrosity; start making a list of adjectives and verbs (properties) for collection and poem.
# TODO Elise: edits to the text - the two pages with fancy font should be added in. and elsewhere. Decide if you want to change multiline titles. How do deal with multiple titles?
# TODO: Elise: find out why we have an odd number of poems
# TODO: practice pulling your text in and exploring it using the terminal
# TODO: upgrade your VS code to make sure GitHub works.
# TODO: Elise: Take your adjectives and/or verbs and write them out in English/Spanish
# TODO: Brandon - figure out why it is ingesting poems as characters and not words


# def self.find_title()
   # """Find the text's title"""
    # get the text
    # get the first line
    # that's the title