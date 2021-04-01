# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.


import glob
import os
import tqdm
from gensim.models.doc2vec import Doc2Vec

from ..analysis import *
from ..utility import *
from ..base import *
from ..tokenizer import *
from ..language import *
from .w_scraper_algorithm_error import *


class Doc2VecHandler:

    algorithm_name = "doc2vec"
    model_file_suffix = ".model"
    corpus_workspace = "doc2vec_corpus"
    corpus_file = "corpus.txt"

    @classmethod
    def build(cls, task_name = None, model_name = None, *, reset = False, config = None):
        if config is None:
            config = Config(task_name)

        algorithm = config.get_parameter(f"model.{model_name}.{'algorithm'}", must = True)
        arguments = config.get_parameter(f"model.{model_name}.{'arguments'}", must = True)

        if algorithm != cls.algorithm_name:
            raise WScraperAlgorithmError(f"Algorithm mismatched. Assumed `{cls.algorithm_name}` but got `{algorithm}`.")

        model_directory = config.make_model_directory()
        model_path = os.path.join(model_directory, model_name + cls.model_file_suffix)

        if not reset and os.path.isfile(model_path):
            sys.stdout.write(f"Model {model_name} already exists. Skipping.\n")
            return

        if "min_count" not in arguments:
            sys.stdout.write("Parameter min_count is not set. Value min_count = 1 is set.\n")
            arguments["min_count"] = 1

        if "workers" not in arguments:
            worker = config.get_worker(must = True)
            sys.stdout.write(f"Parameter workers is not set. wscraper config worker = {worker} is set.\n")
            arguments["workers"] = worker

        tokenizer_property = config.get_tokenizer(must = True)
        tokenizer = Tokenizer.instantiate(tokenizer_property)

        language = Language.get_class(config.get_language(must = True))

        xml_directory = config.get_wikipedia_xml_directory()
        corpus_directory = config.make_workspace(cls.corpus_workspace)

        corpus_writing_flag = True

        corpus_file_path = os.path.join(corpus_directory, cls.corpus_file)

        if os.path.isfile(corpus_file_path):
            if not reset:
                sys.stdout.write(f"A corpus file already exists at {corpus_file_path}. Skipping.\n")
                corpus_writing_flag = False
            else:
                sys.stdout.write(f"A corpus file exists at {corpus_file_path}.\n")
                os.remove(corpus_file_path)
                sys.stdout.write("Removed.\n")

        if corpus_writing_flag:
            sys.stdout.write("Creating a corpus file for doc2vec...\n")
            cls.create_corpus_text(xml_directory, corpus_file_path, language, tokenizer)
            sys.stdout.write("Done!\n")

        sys.stdout.write("Creating a doc2vec model.\n")
        model = cls.create_model(corpus_file_path, ** arguments)
        model.save(model_path)
        sys.stdout.write(f"A doc2vec model was saved to {model_path}.\n")

    @classmethod
    def create_corpus_text(cls, xml_directory, corpus_file_path, language, tokenizer):
        page_iterator = PageIterator(xml_directory)

        with open(corpus_file_path, "w") as writer, tqdm.tqdm(page_iterator) as pager:
            for page in pager:
                pager.set_postfix(OrderedDict(file = f"{page_iterator.i_path}/{page_iterator.n_path}"))
                entry = Parser.page_to_class(page, language = language, entry_only = True)

                if entry is None:
                    continue

                lines = [" ".join(tokenizer.split(sentence)) for sentence in Parser.to_sentences(entry.mediawiki, language = language)]

                writer.write("\n".join(lines))

    @classmethod
    def create_model(cls, corpus_file_path, ** arguments):
        return Doc2Vec(corpus_file = corpus_file_path, ** arguments)

    @classmethod
    def load(cls, path):
        return cls(Doc2Vec.load(path))

    def __init__(self, model):
        self.model = model

    def save(self, path):
        self.model.save(path)

    def save_keyed_vectors(self, path):
        self.model.wv.save(path)
