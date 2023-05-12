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
        # look at how to the matching
        # self.match_poem_with_sibling()
        # self.chiasmus_poems = ???? # for next time with Elise

    def import_collection(self):
        with open(self.filename, 'r') as fin:
            raw_text = fin.read()
        return raw_text

    def convert_raw_text_to_poems(self):
        """Take the raw_text and break it into poems"""
        poems = []
        # within a loop
        # for poem_text in larger_list:
        # do something with poem_text

        for poem_text in self.raw_collection.split('\n\n\n\n'):
            poems.append(Poem(poem_text))
        return poems    

    def find_line_level_chiasmus_over_whole_collection(self):
        for poem in self.poems:
            if poem.has_chiasmus:
                print('=========')
                print(poem.title)
                print(poem.chiasmus_lines)

    def find_poem_level_chiasmus_over_whole_collection(self):
        for poem in self.poems:
            if poem.poem_structure_chiasmus:
                print('=======')
                print('Poem title: ' + poem.title)
                print('First Half:')
                print(poem.first_half)
                print('Second Half:')
                print(poem.second_half)

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
        self.raw_text_as_stanzas = self.raw_stanzas[1:]
        #self.text_without_stopwords
        self.lines_as_stanzas = self.process_raw_stanzas()
        self.lines = [item for sublist in self.lines_as_stanzas for item in sublist]
        self.number_of_lines = len(self.lines)
        self.poem_halves = self.find_poem_halves()
        self.first_half = self.poem_halves[0]
        self.second_half = self.poem_halves[1]
        self.poem_structure_chiasmus = self.find_chiasmus_at_the_poem_level()
        self.chiasmus_lines = self.find_chiasmus_in_poem()
        if len(self.chiasmus_lines) > 0:
            self.has_chiasmus = True
        else:
            self.has_chiasmus = False
    
    def find_chiasmus_at_the_poem_level(self):
        """take the two poem halves and determine if there is chiasmus at the level of the poem's structure"""
        # take the two poem halves
        raw_first_half = ' '.join(self.first_half)
        raw_second_half = ' '.join(self.second_half)
        raw_first_half_tokens = nltk.word_tokenize(raw_first_half)
        raw_second_half_tokens = nltk.word_tokenize(raw_second_half)

        stopwords_list = stopwords.words('english')
        stopwords_list.extend(stopwords.words('spanish'))

        stopped_first_half_tokens = [word for word in raw_first_half_tokens if word not in stopwords_list]
        stopped_second_half_tokens = [word for word in raw_second_half_tokens if word not in stopwords_list]
        return bool(set(stopped_first_half_tokens) & set(stopped_second_half_tokens))
        # modify it to look at individual tokens vs phrases

    def find_poem_halves(self):
        """take the poem and divide into two halves"""
        # break the poem into lines
        lines = self.lines
        # get the number of lines
        number_of_lines = len(lines)
        # use the number of lines to divide the poem in half and that's the midpoint
        midpoint_index = int(number_of_lines / 2)
        # up to the midpoint is the first half
        first_half = lines[:midpoint_index]
        # up to the midpoint is the second half
        second_half = lines[midpoint_index:]
        # send back the two halves
        return (first_half, second_half)

    def convert_poems_into_raw_stanzas(self):
        """Take a poem and split it into stanzas"""
        # this version keeps in punctuation
        # return self.raw_text.split('\n\n\n')
        return self.raw_text_without_punctuation.split('\n\n\n')
    
    def process_raw_stanzas(self):
        lines_in_stanzas = [stanza.split('\n\n') for stanza in self.raw_text_as_stanzas]
        return lines_in_stanzas

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
        stopwords_list.extend(stopwords.words('spanish'))

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

# INSTRUCTIONS FOR PULLING THE THING IN AND WORKING WITH IT
# $ python3
# >>> import salas
# >>> collection = salas.PoetryCollection()
# >>> collection.poems
# >>> collection.poems[0].find_chiasmus_in_poem()
# >>> collection.find_chiasmus_over_whole_collection()

# if you change something, reimport and remake the class
# >>> import importlib
# >>> importlib.reload(salas)
# >>> collection = salas.PoetryCollection()

# TODO Elise: keep annotating this new monstrosity; start making a list of adjectives and verbs (properties) for collection and poem.
# TODO: Elise: practice pulling your text in and exploring it using the terminal
# TODO: Elise: Take your adjectives and/or verbs and write them out in English/Spanish
# TODO: Elise: Think a little more about collection level matching
# TODO: Brandon: change some of the function names to nuance the type of chiasmus we're talking about. Right now we have internal to a poem the usual single word in a line. Next level is at the level of the poem structure. Next level would be the whole collection.
# TODO: Brandon: do translation matching - identify a poem's translation / sibling
# TODO: Brandon: take a look at why the lines in the stanzas haven't been splitting yet

# def self.find_title()
   # """Find the text's title"""
    # get the text
    # get the first line
    # that's the title
