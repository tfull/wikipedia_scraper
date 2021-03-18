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
    def split(cls, name, chunk = 10000):
        if not (type(chunk) == int and chunk in range(100, 10 ** 7 + 1)):
            raise WsError("split: Argument chunk must satisfy 100 <= chunk <= 10 ** 7.")

        config = Config(name)
        wikipedia_xml = config.get_parameter("wikipedia_xml", must = True)
        xml_path = os.path.join(Constant.root_directory, wikipedia_xml)
        cls.split_to_xmls(xml_path, config.xml_directory, chunk)

    @classmethod
    def split_to_xmls(cls, xml_path, output_directory, chunk = 10000):
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
