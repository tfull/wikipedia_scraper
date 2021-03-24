from ..analysis import *
from ..language import *
from ..tokenizer import *
from .w_scraper_algorithm_error import *

import pandas as pd
import tqdm


class WordFrequency:

    algorithm_name = "word_frequency"
    model_file_suffix = ".csv"

    @classmethod
    def build(cls, task_name = None, model_name = None, *, reset = False, config = None):
        if config is None:
            config = Config(task_nmae)

        algorithm = config.get_parameter(f"model.{model_name}.{'algorithm'}", must = True)
        arguments = config.get_parameter(f"model.{model_name}.{'arguments'}", must = True)

        if algorithm != cls.algorithm_name:
            raise ValueError(f"Algorithm mismatched. Assumed `{algorithm_name}` but got `{algorithm}`.")

        xml_directory = config.get_wikipedia_xml_directory()

        tokenizer_property = config.get_tokenizer(must = True)
        tokenizer = Tokenizer.instantiate(tokenizer_property)

        language = Language.get_class(config.get_language(must = True))

        model_directory = config.make_model_directory()

        sys.stdout.write("Building word_frequency model...\n")
        instance = cls.create_count_map(language = language, tokenizer = tokenizer, xml_directory = xml_directory)
        sys.stdout.write("Done.\n")

        output_path = os.path.join(model_directory, model_name + cls.model_file_suffix)
        instance.save(output_path)
        sys.stdout.write(f"Saved to {output_path}.\n")

    @classmethod
    def create_count_map(cls, language, tokenizer, xml_directory):
        document_frequency = {}
        frequency = {}

        for page in tqdm.tqdm(PageIterator(xml_directory)):
            entry = Parser.to_model(page, language = language, entry_only = True)

            if entry is None:
                continue

            words = []

            for sentence in Parser.to_sentences(entry.mediawiki, language = language):
                for word in tokenizer.split(sentence):
                    words.append(word)

                    if word not in frequency:
                        frequency[word] = 1
                    else:
                        frequency[word] += 1

            for word in set(words):
                if word not in document_frequency:
                    document_frequency[word] = 1
                else:
                    document_frequency[word] += 1

        return cls(frequency, document_frequency)

    @classmethod
    def load(cls, path):
        frequency = {}
        document_frequency = {}

        df = pd.read_csv(path)

        for _, row in df.iterrows():
            frequency[row.word] = row.frequency
            document_frequency[row.word] = row.document_frequency

        return cls(frequency, document_frequency)

    def __init__(self, frequency, document_frequency):
        self.frequency = frequency
        self.document_frequency = document_frequency

    def save(self, path):
        records = [(word, self.frequency[word], self.document_frequency[word]) for word in self.frequency.keys()]

        pd.DataFrame(records, columns = ["word", "frequency", "document_frequency"]).to_csv(path, index = False)
