import yaml
import xml.etree.ElementTree


class FileManager:

    @classmethod
    def load_xml(cls, path):
        with open(path, "r") as f:
            parser = xml.etree.ElementTree.XMLParser()

            for line in f:
                parser.feed(line)

            return parser.close()

    @classmethod
    def load_yaml(cls, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

    @classmethod
    def save_yaml(cls, path, data):
        with open(path, "w") as f:
            f.write(yaml.dump(data) + "\n")
