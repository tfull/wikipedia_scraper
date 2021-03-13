import re
import sys
import glob
import os
import xml.etree.ElementTree


class Builder:

    @classmethod
    def split_to_xmls(cls, xml_path, output_directory, *, chunk = 10000):
        re_start = re.compile(r"<page>")
        re_end = re.compile(r"</page>")

        os.makedirs(output_directory, exist_ok = True)

        flag = False
        body = []
        item_n = 0
        file_id = 1

        with open(xml_path, "r") as f:
            for line in f:
                if re_start.search(line):
                    flag = True

                if flag:
                    body.append(line)

                if re_end.search(line):
                    flag = False
                    item_n += 1

                    if item_n % chunk == 0:
                        cls.save_xml(body, "{0}/{1:04d}.xml".format(output_directory, file_id))
                        sys.stdout.write("\033[2K\033[G{0:04d}.xml".format(file_id))
                        sys.stdout.flush()
                        body = []
                        file_id += 1

        if len(body) > 0:
            cls.save_xml(body, "{0}/{1:04d}.xml".format(output_directory, file_id))
            sys.stdout.write("\033[2K\033[G{0:04d}.xml".format(file_id))
            sys.stdout.flush()
        else:
            file_id -= 1

        sys.stdout.write("\033[2K\033[GCompleted: {0} items in {1} files\n".format(item_n, file_id))

    @classmethod
    def save_xml(cls, body, xml_path):
        with open(xml_path, "w") as f:
            f.write("<wikipedia>\n")

            for line in body:
                f.write(line)

            f.write("</wikipedia>\n")

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