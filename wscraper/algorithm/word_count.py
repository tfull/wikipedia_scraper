from ..analysis import *

import pandas as pd
import tqdm


class WordCount:

    def __init__(self):
        self.model = None

    def create(self, xml_directory, language, tokenizer):
        self.model = {}

        for page in tqdm.tqdm(Builder.iterate_page_from_directory(xml_directory)):
            entry = Parser.to_model(page, language = language, entry_only = True)

            if entry is None:
                continue

            for sentence in Parser.to_sentences(entry.mediawiki, language = language):
                for word in tokenizer.split(sentence):
                    if word not in self.model:
                        self.model[word] = 1
                    else:
                        self.model[word] += 1

    def save(self, path):
        pd.DataFrame(self.model.items(), columns = ["word", "count"]).to_csv(path, index = False)

    def load(self, path):
        self.model = {}

        df = pd.read_csv(path)

        for _, row in df.iterrows():
            self.model[row.word] = row.count
