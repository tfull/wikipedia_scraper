import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from wscraper.algorithm.word_count import *
from wscraper.language.japanese import *
from wscraper.tokenizer.mecab_tokenizer import *


def main(directory, output):
    wc = WordCount()
    wc.create(directory, Japanese, MecabTokenizer())
    wc.save(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", required = True, help = "xml directory")
    parser.add_argument("-o", "--output", required = True, help = "path to word count model")

    args = parser.parse_args()

    main(args.dir, args.output)
