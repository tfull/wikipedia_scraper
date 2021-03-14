import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from wscraper.algorithm.word_2_vec_handler import *
from wscraper.language.japanese import *
from wscraper.tokenizer.mecab_tokenizer import *


def main(xml_dir, tmp_dir, output):
    Word2VecHandler.prepare(Japanese, MecabTokenizer(), xml_dir, tmp_dir)
    w2vh = Word2VecHandler.new(tmp_dir)
    w2vh.save(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--xml_dir", required = True, help = "xml directory")
    parser.add_argument("--tmp_dir", required = True, help = "temporary txt directory")
    parser.add_argument("-o", "--output", required = True, help = "/path/to/model")

    args = parser.parse_args()

    main(args.xml_dir, args.tmp_dir, args.output)
