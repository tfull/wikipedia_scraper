import sys
import argparse

from .base import *


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
        sys.stdout.write(help_string.lstrip())
        sys.exit(0)

    name = sys.argv[1]
    args = sys.argv[2:]

    if name in ["initialize", "init"]:
        command_initialize(args)
    elif name == "new":
        command_new(args)
    elif name == "status":
        pass
    elif name == "switch":
        pass
    elif name == "set":
        pass
    else:
        sys.stderr.write(f"No such command {name}.\n\n{help_string}")
        sys.exit(1)


def command_initialize(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper initialize",
        description = "Command `wscraper initialize` creates primary files and directories."
    )

    args = parser.parse_args(args)

    Config.command_initialize()


def command_new(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper new",
        description = "Command `wscraper new` creates task."
    )

    parser.add_argument("name", help = "task name")

    args = parser.parse_args(args)

    Config.command_new(args.name)


def command_import(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper import",
        description = "Command `wscraper import` move a wikipedia.xml file to wscraper directory and split one to small files."
    )

    parser.add_argument("source", help = "source wikipedia.xml file")
    parser.add_argument("-n", "--name", help = "target directory name")
    parser.add_argument("-m", "--move", action = "store_true", help = "move file to wscraper directory for backup")
    parser.add_argument("-c", "--copy", action = "store_true", help = "copy file to wscraper directory for backup")
    parser.add_argument("-r", "--reset", action = "store_true", help = "remove existing file")

    args = parser.parse_args(args)

    if args.move and args.copy:
        sys.stderr.write("Both --move (-m) and --copy (-c) are given.\n")
        sys.exit(1)

    from .analysis.builder import Builder

    Builder.command_import(args.source, args.name, move = args.move, copy = args.copy, reset = args.reset)


def command_switch(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper import",
        description = "Command `wscraper import` move a wikipedia.xml file to wscraper directory and split one to small files."
    )

    parser.add_argument("name", help = "task name")

    args = parser.parse_args(args)

    Config.command_switch(args.name)
