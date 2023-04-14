import nltk
from nltk.corpus import stopwords

class PoetryCollection(object):
    # now create the blueprint for our text object
    def __init__(self, fn):
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

    
class Poem(object):
    """a poem blueprint"""
    def __init__(self, raw_text):
        # self.title
        # what do we want the poem to have?
        # list it out
        self.text = raw_text
        # self.text_without_punctuation
        #self.text_without_stopwords
        # self.does_it_have_chiasmus?
        self.stanzas = self.convert_poems_into_stanzas()
        self.chiasmus_lines = self.find_chiasmus_in_poem()
        if len(self.chiasmus_lines) > 0:
            self.has_chiasmus = True
        else:
            self.has_chiasmus = False


    def convert_poems_into_stanzas(self):
        """Take a poem and split it into stanzas"""
        return self.text.split('\n\n\n')
    
    def convert_stanzas_into_lines(self):
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
        raw_lines_ish = self.text.split('\n')
        results = []
        for line in raw_lines_ish:
            line_halves = self.line_midpoint(line)
            if self.find_chiasmus_in_line_using_simple_token_matching(line_halves):
                results.append(line)
                print(line)
                # results.append((line,line_halves))
        return results

# >>> import salas
# >>> collection = salas.PoetryCollection('antes.txt')
# >>> collection.poem

# TODO Elise: take out frontmatter and epigraph; finish dividing poem; read cookbook chapter; annotate this new monstrosity; come up with a function; start making a list of adjectives and verbs (properties) for collection and poem. Do the template-y class example.
# TODO: Brandon - finish this file conversion.