from wscraper.analysis import *


for i, e in enumerate(EntryIterator()):
    print(i, e.title)
