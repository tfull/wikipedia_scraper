# coding: utf-8

import re
import sys
from io import StringIO
import Information

DEBUG_1 = False
DEBUG_2 = False

RE_08 = re.compile(r"<!--.*?-->", re.DOTALL)
RE_19 = re.compile(r"<nowiki>.*?</nowiki>", re.DOTALL)
RE_01 = re.compile(r"\{\{[^\{]*?\}\}")
RE_02 = re.compile(r"\{\|.*?\|\}", re.DOTALL)
RE_07 = re.compile(r"<ref[^>]*/>")
RE_03 = re.compile(r"<ref[^>]*>.*?</ref>", re.DOTALL)
RE_12 = re.compile(r"<math>.*?</math>", re.DOTALL)
RE_18 = re.compile(r"<code>.*?</code>", re.DOTALL)
RE_04 = re.compile(r"\'{2,}")

RE_05 = re.compile(r"\[\[[^\[]*?\]\]")
RE_06 = re.compile(r"\[\[(.*?)\|(.*?)\]\]")

RE_11 = re.compile(r"\[[^\[]*?\]")

RE_09 = re.compile(r"={2,}(.*?)={2,}")

RE_10 = re.compile(r"\n\W*\n")

RE_13 = re.compile(r"<div(?: .*?)?>(.*?)</div>")
RE_14 = re.compile(r"<span(?: .*?)?>(.*?)</span>")
RE_15 = re.compile(r"<sub>(.*?)</sub>")
RE_16 = re.compile(r"<sup>(.*?)</sup>")
RE_17 = re.compile(r"<([a-z]+)(?: .*?)?>.*?</\1>")

def parse_media_wiki(text):
    link_to = []
    categories = []

    if DEBUG_1:
        sys.stderr.write("[Source]: " + text + "\n")
        sys.stderr.flush()
    text = re.sub(RE_08, "", text)
    text = re.sub(RE_19, "", text)
    for i in range(5):
        text = re.sub(RE_01, "", text)
    text = re.sub(RE_02, "", text)
    text = re.sub(RE_07, "", text)
    text = re.sub(RE_03, "", text)
    text = re.sub(RE_12, "", text)
    text = re.sub(RE_18, "", text)
    text = re.sub(RE_04, "", text)
    if DEBUG_1:
        sys.stderr.write("[Cleaned]: " + text + "\n")
        sys.stderr.flush()

    while True:
        match = re.search(RE_17, text)
        if match == None:
            break
        m = re.match(RE_13, match.group())
        if m:
            text = text[:match.start()] + m.group(1) + text[match.end():]
            continue
        m = re.match(RE_14, match.group())
        if m:
            text = text[:match.start()] + m.group(1) + text[match.end():]
            continue
        m = re.match(RE_15, match.group()) or re.match(RE_16, match.group())
        if m:
            text = text[:match.start()] + m.group(1) + text[match.end():]
            continue
        if DEBUG_2:
            sys.stderr.write(match.group(1) + "\n")
        text = text[:match.start()] + match.group(1) +  text[match.end():]

    while True:
        match = re.search(RE_05, text)
        if match == None:
            break
        inlink = re.match(RE_06, match.group())
        surface = None
        link = None
        if inlink != None:
            surface = inlink.group(2)
            link = inlink.group(1)
        else:
            surface = match.group()[2:-2]
            link = surface
        flag = True
        if link[:9] == "Category:":
            categories.append(link[9:])
            flag = False
        else:
            for ns in Information.NAMESPACES:
                if link[:len(ns) + 1] == ns + ":":
                    flag = False
        if flag:
            link_to.append(link)
            text = text[:match.start()] + surface + text[match.end():]
        else:
            text = text[:match.start()] + text[match.end():]

    while True:
        match = re.search(RE_11, text)
        if match == None:
            break
        text = text[:match.start()] + text[match.end():]

    document = text_to_document(text)

    return (document, link_to, categories)

def text_to_document(text):
    io = StringIO(text)
    d = { "abstract": "" }
    sec = "abstract"
    ignore = False
    extra = [ "References", "External links", "Further reading", "See also" ]

    for line in io.readlines():
        m = re.match(RE_09, line)
        if m != None:
            mg1 = m.group(1).strip()
            if mg1 in extra:
                ignore = True
            else:
                ignore = False
                sec = mg1
                d[sec] = ""
        else:
            if ignore:
                pass
            else:
                d[sec] += line.lstrip("*")

    for key in list(d.keys()):
        s = condense_text(d[key]).replace("\n", " ").strip()
        if len(s) == 0:
            del d[key]
        else:
            d[key] = s

    return d

def condense_text(text):
    text = re.sub(RE_10, "\n", text)
    return text
