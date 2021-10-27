# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

from .parser import *
from .entry_iterator import *


class DocumentIterator:

    def __init__(self, name = None, tagger = None, *, language = None):
        self.entry_iterator = EntryIterator(name = name, language = language)
        self.language = self.entry_iterator.both_iterator.language
        self.tagger = tagger

    def __iter__(self):
        self.entry_iterator.__iter__()
        return self

    def __next__(self):

        while True:
            entry = next(self.entry_iterator)

            text = Parser.to_plain_text(entry.mediawiki, language = self.language)

            if self.tagger is None:
                doc = text
            else:
                doc = self.tagger(text)

            if doc is not None:
                return doc
