import glob
from gensim.models.word2vec import Word2Vec

from ..analysis import *
from ..utility import *


class Word2VecHandler:

    @classmethod
    def prepare(cls, xml_directory, txt_directory):
        with FileWriter(txt_directory, "{:06d}.txt", 10000) as writer:
            for page in PageIterator(xml_directory):
                Parser.to_model(page, language = language, entry_only = True)

                if entry is None:
                    continue

                lines = [" ".join(tokenizer.split(sentence)) for sentence in Parser.to_sentences(entry.mediawiki)]

                writer.write("\n".join(lines), len(lines))

    @classmethod
    def new(cls, language, tokenizer, txt_directory):
        model = None

        for txt_file in sorted(glob.glob(txt_directory + "/*.txt")):
            sentences = [tokenizer.rstrip("\n").split(" ") for line in txt_file]

            if model is None:
                model = Word2Vec(sentences, min_count = 1)
            else:
                model.build_vocab(sentences, update = True)
                model.train(sentences, total_examples = model.corpus_count, epochs = model.epochs)

        return cls(model)

    @classmethod
    def load(cls, path):
        return cls(Word2Vec.load(path))

    def __init__(self, model):
        self.model = model

    def save(self, path):
        self.model.save(path)
