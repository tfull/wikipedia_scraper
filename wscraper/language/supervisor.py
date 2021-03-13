class Supervisor:

    @classmethod
    def get_language_class(cls, name):
        if name == "ja":
            from .japanese import Japanese
            return Japanese
        else:
            from .english import English
            return English
