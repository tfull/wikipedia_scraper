from gensim.models.word2vec import Word2Vec

from ..analysis import *


class Word2VecHandler:

    @classmethod
    def prepare(cls, xml_directory, txt_directory):
        with FileWriter(txt_directory, "{:06d}.txt", 10000) as writer:
            for page in Builder.iterate_page_from_directory(xml_directory):
                Parser.to_model(page, language = language, entry_only = True)

                if entry is None:
                    continue

                lines = [" ".join(tokenizer.split(sentence)) for sentence in Parser.to_sentences(entry.mediawiki)]

                writer.write("\n".join(lines), len(lines))

    def __init__(self):
        self.model = None

    def create(self, language, tokenizer, xml_directory, txt_directory):
        for page in Builder.iterate_page_from_directory(xml_directory):
            entry = Parser.to_model(page, language = language, entry_only = True)

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
