from wscraper.analysis import *


for i, b in enumerate(BothIterator()):
    print(f"both: {i}: {type(b)}")

for i, e in enumerate(EntryIterator()):
    print(f"entry {i}: {e.title} {len(e.mediawiki)}")

for i, r in enumerate(RedirectionIterator()):
    print(f"redirection: {i}: {r.source} -> {r.target}")
