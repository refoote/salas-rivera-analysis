import nltk
from nltk.corpus import stopwords
from nltk.text import Text
import string
import pylab

class TreatAsOneText(object):
    def __init__(self, fn='antes_linebreak.txt'):
        """
        import salas
        text = salas.TreatAsOneText()
        text.make_the_plot()
        to change the words tracked you would modify WORDS_TO_PLOT below and reload like so.
        importlib.reload(salas)
        text = salas.TreatAsOneText()
        text.make_the_plot()
        """
        self.filename = fn
        self.raw_text = self.import_collection()
        self.cleaned_text = [word.lower() for word in self.raw_text]
        self.nltk_text = Text(nltk.word_tokenize(self.raw_text))
        #########
        self.WORDS_TO_PLOT = ['puerto', 'rico', 'isla', 'island']
        #########
        
    def make_the_plot(self):
        self.nltk_text.dispersion_plot(self.WORDS_TO_PLOT)
        pylab.show()

    def import_collection(self):
        with open(self.filename, 'r') as fin:
            raw_text = fin.read()
        return raw_text

class PoetryCollection(object):
    # now create the blueprint for our text object
    def __init__(self, fn='antes_linebreak.txt'):
        # given a filename, store it
        self.filename = fn
        self.raw_collection = self.import_collection()
        self.poems = self.convert_raw_text_to_poems()
        self.match_translations()

    def match_translations(self):
        """Loop over poems and match indices with translations"""
        num_poems = len(self.poems)
        
        for poem_index, poem in enumerate(self.poems):
            translation_index = num_poems-poem_index
            poem.assign_translation_index(translation_index)
            poem.assign_translation(self.poems[translation_index-1])

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
            if poem.has_line_level_chiasmus:
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

    def find_bilinear_chiasmus_over_whole_collection(self):
        for poem in self.poems:
            if poem.has_bilinear_chiasmus:
                print('=====')
                print(poem.title)
                print(poem.bilinear_chiasmus_lines)

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
            self.has_line_level_chiasmus = True
        else:
            self.has_line_level_chiasmus = False
        self.has_bilinear_chiasmus = False
        self.find_bilinear_chiasmus()

    def find_bilinear_chiasmus(self):
        self.bilinear_chiasmus_lines = []
        for line_index, line in enumerate(self.lines):
            if line_index < len(self.lines)-1:
                first_in_line_pair = line
                second_in_line_pair = self.lines[line_index+1]
                first_quarter, second_quarter = self.line_midpoint(first_in_line_pair)
                third_quarter, fourth_quarter = self.line_midpoint(second_in_line_pair)
                if self.find_chiasmus_in_line_using_simple_token_matching((first_quarter, fourth_quarter)) or self.find_chiasmus_in_line_using_simple_token_matching((second_quarter, third_quarter)):
                    self.has_bilinear_chiasmus = True
                    self.bilinear_chiasmus_lines.append([first_in_line_pair,second_in_line_pair])

    def assign_translation_index(self, translation_pos):
        self.translation_index = translation_pos

    def assign_translation(self, poem_translation):
        self.translation = poem_translation
        self.translation_title = self.translation.title

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
# >>> collection.find_line_level_chiasmus_over_whole_collection()

# if you change something, reimport and remake the class
# >>> import importlib
# >>> importlib.reload(salas)
# >>> collection = salas.PoetryCollection()

# TODO Elise: start making a list of adjectives and verbs (properties) for collection and poem.
# TODO: Elise: practice pulling your text in and exploring it using the terminal
# TODO: Elise: Take your adjectives and/or verbs and write them out in English/Spanish
# TODO: think about the things you need for the article - do you have the graphs you need.
# TODO: Brandon: finish up the class to get a frequency distribution across the whole text

# def self.find_title()
   # """Find the text's title"""
    # get the text
    # get the first line
    # that's the title
  