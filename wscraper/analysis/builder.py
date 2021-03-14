from ..utility import *

import re
import sys
import glob
import os
import tqdm
import xml.etree.ElementTree
from collections import OrderedDict


class Builder:

    @classmethod
    def split_to_xmls(cls, xml_path, output_directory, *, chunk = 10000):
        re_start = re.compile(r"<page>")
        re_end = re.compile(r"</page>")

        os.makedirs(output_directory, exist_ok = True)

        flag = False
        body = []

        reader = open(xml_path, "r")
        writer = FileWriter(output_directory, "{:04d}.xml", chunk, prefix = "<wikipedia>\n", suffix = "</wikipedia>\n")

        with tqdm.tqdm(reader) as progress:
            with reader, writer:
                for line in progress:
                    progress.set_postfix(OrderedDict(entry = writer.total_count, page = writer.file_count))

                    if re_start.search(line):
                        flag = True

                    if flag:
                        body.append(line)

                    if re_end.search(line):
                        flag = False
                        writer.write("".join(body), count = 1)
                        body = []

            progress.set_postfix(OrderedDict(entry = writer.total_count, page = writer.file_count))

    @classmethod
    def load_xml(cls, xml_path):
        with open(xml_path, "r") as f:
            parser = xml.etree.ElementTree.XMLParser()

            for line in f:
                parser.feed(line)

            return parser.close()

    @classmethod
    def list_pages(cls, xml_path):
        tree = cls.load_xml(xml_path)
        return tree.findall("page")

    @classmethod
    def iterate_page_from_directory(cls, directory):
        for xml in sorted(glob.glob(directory + "/*.xml")):
            for page in cls.list_pages(xml):
                yield page

    @classmethod
    def iterate_pages_from_directory(cls, directory):
        for xml in sorted(glob.glob(directory + "/*.xml")):
            yield (xml.split("/")[-1][:-4], cls.list_pages(xml))
