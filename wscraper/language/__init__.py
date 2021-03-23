class Language:

    @classmethod
    def get_class(cls, name):
        if name == "japanese":
            from .japanese import Japanese
            return Japanese
        elif name == "english":
            from .english import English
            return English
        else:
            raise WScraperLanguageError(f"Language `{name}` is not implemented.")


class WScraperLanguageError(Exception):
    pass
