from ..utility import *

import glob


class PageIterator:

    def __init__(self, xml_directory):
        self.path_list = sorted(glob.glob(xml_directory + "/*.xml"))
        self.i_path = 0
        self.page_list = []
        self.i_page = 0

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.page_list) == 0:
            if len(self.path_list) == 0:
                raise StopIteration()

            path = self.path_list.pop(0)
            self.page_list = FileManager.load_xml(path).findall("page")

        return self.page_list.pop(0)
