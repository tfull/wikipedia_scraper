# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.


class Tokenizer:

    @classmethod
    def instantiate(cls, tokenizer_property):
        name = tokenizer_property["name"]
        arguments = tokenizer_property["arguments"]

        if name == "mecab":
            from .mecab_tokenizer import MecabTokenizer
            return MecabTokenizer(** arguments)
        elif name == "janome":
            from .janome_tokenizer import JanomeTokenizer
            return JanomeTokenizer(** arguments)
        else:
            raise WScraperTokenizerError(f"No such tokenizer {name}.")
