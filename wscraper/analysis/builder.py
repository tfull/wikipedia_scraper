from ..utility import *
from ..base import *

import re
import sys
import glob
import os
import tqdm
from collections import OrderedDict


class Builder:

    @classmethod
    def split(cls, name = None, *, reset = False, chunk = 10000):
        if not (type(chunk) == int and chunk in range(100, 10 ** 7 + 1)):
            raise WsError("Argument chunk must satisfy 100 <= chunk <= 10 ** 7.")

        config = Config(name)
        wikipedia_xml = config.get_wikipedia_xml()
        wikipedia_xml_directory = config.get_wikipedia_xml_directory()

        if os.path.isdir(wikipedia_xml_directory):
            if not reset:
                sys.stdout.write("Split XML files are already exist. Skipping.\n")
                return
            else:
                sys.stdout.write("Split XML files are exist. Removing.\n")
                for path in glob.glob(os.path.join(wikipedia_xml_directory, "*.xml")):
                    os.remove(path)
        else:
            os.makedirs(wikipedia_xml_directory)

        sys.stdout.write(f"Split Wikipedia XML file {wikipedia_xml} to {wikipedia_xml_directory}.\n")
        cls.split_to_xmls(wikipedia_xml, wikipedia_xml_directory, chunk = chunk)
        sys.stdout.write("Done!\n")

    @classmethod
    def split_to_xmls(cls, xml_path, output_directory, *, chunk = 10000):
        re_start = re.compile(r"<page>")
        re_end = re.compile(r"</page>")

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
