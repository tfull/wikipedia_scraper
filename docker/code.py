from wscraper.analysis import *
from wscraper.language import *


def tagger(x):
    return x.strip().split()

language = Language.get_class("japanese")

for i, b in enumerate(BothIterator()):
    print(f"both: {i}: {type(b)}")

for i, e in enumerate(EntryIterator()):
    print(f"entry {i}: {e.title} {len(e.mediawiki)}")

for i, r in enumerate(RedirectionIterator()):
    print(f"redirection {i}: {r.source} -> {r.target}")

for i, d in enumerate(ArticleIterator(tagger = tagger)):
    print(f"article {i}: {' '.join(d[:10])[:32]}")
