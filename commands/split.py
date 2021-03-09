import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from main.core import *


def main(xml_path, output_directory):
    Builder.split(xml_path, output_directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--xml", required = True, help = "wikipedia-dump.xml")
    parser.add_argument("-o", "--dir", required = True, help = "output directory")

    args = parser.parse_args()

    main(args.xml, args.dir)
