# coding: utf-8

import xml.etree.ElementTree as E
import MediaWiki
import Information
import sys
import re
import mysql.connector
from nltk.stem import WordNetLemmatizer

DEBUG = False

LEMMATIZER = WordNetLemmatizer()

RE_01 = re.compile(r"[^a-zA-Z0-9]")

def lemmatize(w):
    w = LEMMATIZER.lemmatize(w)
    return LEMMATIZER.lemmatize(w, "v")

def insert(cursor, page):
    title = page.find("title").text
    redirect = page.find("redirect")

    for rm in Information.NAMESPACES:
        if title[:len(rm) + 1] == rm + ":":
            # sys.stderr.write(title + ": deleted\n")
            return

    if redirect != None:
        if "title" not in redirect.attrib:
            # sys.stderr.write(title + ": title not in redirect\n")
            return
        cursor.execute("insert into redirections (origin, target) values (%s, %s)", (title, redirect.attrib["title"]))
    else:
        revision = page.find("revision")
        text = revision.find("text")
        if text == None or text.text == None:
            # sys.stderr.write("{1}: text is None\n".format(title))
            return
        (sections, links, categories) = MediaWiki.parse_media_wiki(text.text.replace("&nbsp;", " "))
        doc = " ".join([lemmatize(w) for t in sections for w in re.sub(RE_01, " ", sections[t]).lower().split()])
        cursor.execute("insert into entries (title, document, link, category) values (%s, %s, %s, %s)", (title, doc, "|".join(links), "|".join(categories)))

def read(cursor, path):
    with open(path, "r") as f:
        parser = E.XMLParser()
        for line in f:
            parser.feed(line)
        tree = parser.close()
        for page in tree.findall("page"):
            insert(cursor, page)

def main(host, db, user, passwd, paths):
    connection = mysql.connector.connect(host=host, db=db, user=user, passwd=passwd, charset="utf8")
    cursor = connection.cursor()
    for path in paths:
        print(path)
        read(cursor, path)
        connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    args = sys.argv
    main(args[1], args[2], args[3], args[4], args[5:])
