class WScraperException(Exception):
    pass


class WScraperConfigError(WScraperException):
    pass


class WScraperAlgorithmError(WScraperException):
    pass


class WScraperLanguageError(WScraperException):
    pass


class WScraperTokenizerError(WScraperException):
    pass
