from janome.tokenizer import Tokenizer


class JanomeTokenizer:

    def __init__(self):
        self.tokenizer = Tokenizer()

    def split(self, sentence):
        return self.tokenizer.tokenize(sentence, wakati = True)
