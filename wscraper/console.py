import sys

from .base.ws_error import *


help_string = """
wscraper

Wikipedia Scraper
    language model using Wikipedia

command:
    wscraper initialize
        make directory ~/.wscraper and config file
    wscraper init
        same as initialize
    wscraper new [name]
        create pattern named [name]
"""


def command():
    if len(sys.argv) < 2:
        return sys.stderr.write(help_string.lstrip())

    name = sys.argv[1]
    args = sys.argv[2:]

    if name in ["initialize", "init"]:
        import .command.initialize as m
        m.run(args)
    elif name == "new":
        import .command.new as m
        m.run(args)
    elif name == "status":
        pass
    elif name == "switch":
        pass
    elif name == "set":
        pass
    else:
        raise WsError(f"No such command \"{name}\".")
