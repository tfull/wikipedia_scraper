from gensim.models.word2vec import Word2Vec

from ..analysis import *


class Word2VecHandler:

    def __init__(self):
        self.model = None

    def create(self, xml_directory, tokenizer):
        for page in Builder.iterate_page_from_directory(xml_directory):
            entry = Parser.to_model(page, entry_only = True)

            if entry is None:
                continue

            sentences = [tokenizer.split(sentence) for sentence in Parser.to_sentences(entry.mediawiki)]

            if self.model is None:
                self.model = Word2Vec(sentences, min_count = 1)
            else:
                self.model.build_vocab(sentences, update = True)
                self.model.train(sentences, total_examples = self.model.corpus_count, epochs = self.model.epochs)

    def save(self, path):
        self.model.save(path)

    def load(self, path):
        self.model = Word2Vec.load(path)
