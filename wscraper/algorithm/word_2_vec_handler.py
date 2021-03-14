import glob
import os
from gensim.models.word2vec import Word2Vec, PathLineSentences

from ..analysis import *
from ..utility import *


class Word2VecHandler:

    @classmethod
    def prepare(cls, language, tokenizer, xml_directory, txt_directory):
        os.makedirs(txt_directory)

        with FileWriter(txt_directory, "{:06d}.txt", 10000) as writer:
            for page in PageIterator(xml_directory):
                entry = Parser.to_model(page, language = language, entry_only = True)

                if entry is None:
                    continue

                lines = [" ".join(tokenizer.split(sentence)) for sentence in Parser.to_sentences(entry.mediawiki, language = language)]

                writer.write("\n".join(lines), len(lines))

    @classmethod
    def new(cls, txt_directory):
        model = Word2Vec(PathLineSentences(txt_directory), min_count = 1)
        return cls(model)

    @classmethod
    def load(cls, path):
        return cls(Word2Vec.load(path))

    def __init__(self, model):
        self.model = model

    def save(self, path):
        self.model.save(path)
