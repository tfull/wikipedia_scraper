from ..model import *
from ..utility import *

import re


RE_COMMENT    = re.compile(r"<!--.*?-->", re.DOTALL)
RE_NOWIKI     = re.compile(r"<nowiki>.*?</nowiki>", re.DOTALL)
RE_BRACKET_1  = re.compile(r"\{[^\{]*?\}")
RE_BRACKET_2  = re.compile(r"\{\{([^\{]*?)\}\}")
RE_REF_SINGLE = re.compile(r"<ref[^>]*/>")
RE_REF_PAIR   = re.compile(r"<ref[^>]*>.*?</ref>", re.DOTALL)
RE_PRIME      = re.compile(r"\'{2,}")
RE_TAG        = re.compile(r"<([a-zA-Z]+)(.*?)?>(.*?)</\1>")
RE_LINK       = re.compile(r"\[\[([^\[]*?)\]\]")
RE_SQ         = re.compile(r"\[[^\[]*?\]")
RE_CHAPTER    = re.compile(r"={2,}(.*?)={2,}")
RE_LIST       = re.compile(r"\* ")


class Parser:

    @classmethod
    def to_model(cls, page, *, language = None, entry_only = False):
        if language is None:
            raise ValueError("language: None")

        title = page.find("title").text

        for rm in language.exclusive_title:
            if title.startswith(rm + ":"):
                return None

        redirect = page.find("redirect")

        if redirect is not None:
            if entry_only:
                return None
            else:
                target = redirect.attrib["title"]
                return Redirection(source = title, target = target)

        revision = page.find("revision")
        text = revision.find("text").text

        if text is None:
            return None

        text = "".join(filter(lambda c: ord(c) < 0x10000, text))

        return Entry(title = title, mediawiki = text)

    @classmethod
    def interpret_mediawiki(cls, mediawiki, *, language = None):
        if language is None:
            raise ValueError("language: None")

        text = mediawiki

        text = re.sub(RE_COMMENT, "", text)
        text = re.sub(RE_NOWIKI, "", text)

        while True:
            match = re.search(RE_BRACKET_2, text)

            if match is None:
                break

            text = text[: match.start()] + language.bracket_to_surface(match) + text[match.end() :]

        text = re.sub(RE_BRACKET_1, "", text)
        text = re.sub(RE_REF_SINGLE, "", text)
        text = re.sub(RE_REF_PAIR, "", text)
        text = re.sub(RE_PRIME, "", text)

        text = text.replace("__TOC__", "").replace("&amp;", "&")

        while True:
            match = re.search(RE_TAG, text)

            if match is None:
                break

            text = text[: match.start()] + language.tag_to_surface(match) + text[match.end() :]

        while True:
            match = re.search(RE_LINK, text)

            if match is None:
                break

            text = text[: match.start()] + language.link_to_surface(match) + text[match.end() :]

        return text

    @classmethod
    def to_plain_text(cls, mediawiki, *, language = None):
        if language is None:
            raise ValueError("language: None")

        text = cls.interpret_mediawiki(mediawiki, language = language)
        lines = []

        for line in text.split("\n"):
            if len(line) == 0:
                continue

            if line.startswith("* "):
                lines.append(line[2:])
            else:
                match = re.match(RE_CHAPTER, line)

                if match:
                    pass
                else:
                    lines.append(line)

        return "\n".join(lines)

    @classmethod
    def to_paragraphs(cls, mediawiki, *, language = None):
        if language is None:
            raise ValueError("language: None")

        text = cls.interpret_mediawiki(mediawiki, language = language)
        lines = text.split("\n")

        paragraphs = []
        lines_stock = []
        previous = "*"

        for line in lines:
            match = re.match(RE_CHAPTER, line)

            if match:
                paragraphs.append((previous, "\n".join(lines_stock)))
                previous = match.group(1)
                lines_stock = []
            elif len(line) > 0:
                if line.startswith("* "):
                    lines_stock.append(line[2:])
                else:
                    lines_stock.append(line)

        paragraphs.append((previous, "\n".join(lines_stock)))

        return [(title, document) for title, document in paragraphs if len(document) > 0]

    @classmethod
    def to_sentences(cls, mediawiki, *, language = None):
        if language is None:
            raise ValueError("language: None")

        plain_text = cls.to_plain_text(mediawiki, language = language)

        return language.document_to_sentences(plain_text)
