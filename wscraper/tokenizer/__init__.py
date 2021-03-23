class Tokenizer:

    @classmethod
    def get_by_property(tokenizer_property):
        name = tokenizer_property["name"]

        if name == "mecab":
            from .mecab_tokenizer import MecabTokenizer
            return MecabTokenizer(tokenizer_property["arguments"])
        elif name == "janome":
            from .janome_tokenizer import JanomeTokenizer
            return JanomeTokenizer(tokenizer_property[""])
        else:
            raise WsError(f"No such tokenizer {name}.")
