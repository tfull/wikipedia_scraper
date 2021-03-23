import glob
import os
from gensim.models.word2vec import Word2Vec, PathLineSentences

from ..analysis import *
from ..utility import *
from ..base import *
from ..tokenizer import *
from ..language import *


class Word2VecHandler:

    model_file_suffix = ".model"

    @classmethod
    def build(cls, task_name = None, model_name = None, *, reset = False, config = None):
        if config is None:
            config = Config(task_name)

        arguments = config.get_parameter(f"model.{model_name}.{'arguments'}", must = True)

        tokenizer_property = config.get_tokenizer(must = True)
        tokenizer = Tokenizer.instantiate(tokenizer_property)

        language = Language.get_class(config.get_language(must = True))

        xml_directory = config.get_wikipedia_xml_directory()
        pls_directory = config.make_workspace("pls")
        model_directory = config.make_model_directory()

        pls_flag = True

        existing_files = glob.glob(os.path.join(pls_directory, "*.txt"))

        if len(existing_files) > 0:
            if not reset:
                sys.stdout.write(f"Path line sentences already exist at {pls_directory}. Skipping.\n")
                pls_flag = False
            else:
                sys.stdout.write(f"Path line sentences exist at {pls_directory}. Removing.\n")
                for path in existing_files:
                    os.path.remove(path)
                sys.stdout.write("Removed.\n")

        if pls_flag:
            cls.create_path_line_sentences(xml_directory, pls_directory, language, tokenizer)

        sys.stdout.write("Creating Word2Vec model.\n")
        model_path = os.path.join(model_directory, model_name + cls.model_file_suffix)
        model = cls.create_model(pls_directory)
        model.save(model_path)
        sys.stdout.write(f"Word2Vec model was saved to {model_path}.\n")

    @classmethod
    def create_path_line_sentences(cls, xml_directory, pls_directory, language, tokenizer):
        with FileWriter(pls_directory, "{:06d}.txt", 10000) as writer:
            for page in PageIterator(xml_directory):
                entry = Parser.to_model(page, language = language, entry_only = True)

                if entry is None:
                    continue

                lines = [" ".join(tokenizer.split(sentence)) for sentence in Parser.to_sentences(entry.mediawiki, language = language)]

                writer.write("\n".join(lines), len(lines))

    @classmethod
    def create_model(cls, pls_directory, ** arguments):
        if "min_count" not in arguments:
            arguments["min_count"] = 1

        model = Word2Vec(PathLineSentences(pls_directory), ** arguments)
        return model

    @classmethod
    def load(cls, path):
        return cls(Word2Vec.load(path))

    def __init__(self, model):
        self.model = model

    def save(self, path):
        self.model.save(path)

    def save_keyed_vectors(self, path):
        self.model.wv.save(path)
