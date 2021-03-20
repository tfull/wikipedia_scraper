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
    def split(cls, name, *, reset = False, chunk = 10000):
        if not (type(chunk) == int and chunk in range(100, 10 ** 7 + 1)):
            raise WsError("split: Argument chunk must satisfy 100 <= chunk <= 10 ** 7.")

        config = Config(name)
        wikipedia_name = config.get_parameter("wikipedia", must = True)
        xml_directory = os.path.join(Constant.wikipedia_directory, wikipedia_name)

        wikipedia_xml = os.path.join(Constant.wikipedia_directory, f"{wikipedia_name}.xml")

        if os.path.isfile(wikipedia_xml):
            raise WsError(f"split: Wikipedia XML file {wikipedia_name}.xml does not exist in {Constant.wikipedia_directory}.")

        if os.path.isdir(xml_directory):
            if not reset:
                return
            else:
                for path in glob.glob(os.path.join(xml_directory, "*.xml")):
                    os.remove(path)
        else:
            os.makedirs(xml_directory)

        cls.split_to_xmls(wikipedia_xml, xml_directory, chunk)

    @classmethod
    def split_to_xmls(cls, xml_path, output_directory, chunk = 10000):
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
