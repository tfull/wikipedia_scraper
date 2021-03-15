import xml.etree.ElementTree


class FileManager:

    @classmethod
    def load_xml(cls, xml_path):
        with open(xml_path, "r") as f:
            parser = xml.etree.ElementTree.XMLParser()

            for line in f:
                parser.feed(line)

            return parser.close()
