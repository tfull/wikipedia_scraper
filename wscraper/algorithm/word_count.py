from ..analysis import *

import pandas as pd
import tqdm


class WordCount:

    @classmethod
    def new(cls, language, tokenizer, xml_directory):
        model = {}

        for page in tqdm.tqdm(PageIterator(xml_directory)):
            entry = Parser.to_model(page, language = language, entry_only = True)

            if entry is None:
                continue

            for sentence in Parser.to_sentences(entry.mediawiki, language = language):
                for word in tokenizer.split(sentence):
                    if word not in model:
                        model[word] = 1
                    else:
                        model[word] += 1

        return cls(model)

    @classmethod
    def load(cls, path):
        model = {}

        df = pd.read_csv(path)

        for _, row in df.iterrows():
            model[row.word] = row.count

        return cls(model)

    def __init__(self, model):
        self.model = model

    def save(self, path):
        pd.DataFrame(self.model.items(), columns = ["word", "count"]).to_csv(path, index = False)
