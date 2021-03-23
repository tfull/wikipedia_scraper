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
        command_status(args)
    elif name == "switch":
        command_switch(args)
    elif name == "set":
        command_set(args)
    elif name == "model":
        command_model(args)
    elif name == "root":
        command_root(args)
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


def command_status(args):
    if len(args) != 0:
        sys.stderr.write("No arguments required for `wscraper status`.")
        sys.exit(1)

    Config.command_status()


def command_model(args):
    if len(args) == 0:
        sys.stderr.write("Few arguments for wscraper model.\n")
        sys.stderr.write("wscraper model [name] [arguments]\n")
        sys.exit(1)

    name = args[0]
    args = args[1:]

    if name == "new":
        command_model_new(args)
    elif name == "delete":
        command_model_delete(args)
    elif name == "build":
        command_model_build(args)
    else:
        sys.stderr.write(f"No such command {name} for wscraper model.\n")
        sys.exit(1)


def command_model_new(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper model new",
        description = "Command `wscraper model new` creates model status."
    )

    parser.add_argument("name", help = "your favorite name for model")
    parser.add_argument("algorithm", help = "model algorithm")

    args = parser.parse_args(args)

    Config.command_model_new(args.name, args.algorithm)


def command_model_delete(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper model delete",
        description = "Command `wscraper model delete` creates model status."
    )

    parser.add_argument("name", help = "your favorite name for model")

    args = parser.parse_args(args)

    Config.command_model_delete(args.name)


def command_model_build(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper model build",
        description = "Command `wscraper model build` creates models for preserved algorithms and arguments."
    )

    parser.add_argument("name", nargs="*", help = "model name. Nothing indicates all models.")
    parser.add_argument("-r", "--reset", action = "store_true", help = "truncate existing models")

    args = parser.parse_args(args)

    from .algorithm import Algorithm

    Algorithm.command_build(args.name)


def command_root(args):
    if len(args) == 0:
        sys.stderr.write("wscraper root\n\n")
        sys.stderr.write("  wscraper root status\n")
        sys.stderr.write("  wscraper root set [options]\n")
        sys.stderr.write("  wscraper root delete [options]\n")
        sys.exit(1)

    name = args[0]

    if name == "status":
        command_root_status(args[1:])
    elif name == "set":
        command_root_set(args[1:])
    elif name == "delete":
        command_root_delete(args[1:])
    else:
        sys.stderr.write(f"No such command {name}.\n")
        sys.stderr.write("Command `wscraper root` takes `status`, `set` or `delete` for first argument.\n")
        sys.exit(1)


def command_root_status(args):
    if len(args) != 0:
        sys.stderr.write("No arguments required for `wscraper root status`.\n")
        sys.exit(1)

    Config.command_root_status()


def command_root_set(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper root set",
        description = "Command `wscraper root` describes or changes default value."
    )

    parser.add_argument("--wikipedia", help = "Wikipedia name")
    parser.add_argument("--worker", help = "the number of threads for working")
    parser.add_argument("--language", help = "Wikipedia language")

    args = parser.parse_args(args)

    Config.command_root_set(wikipedia = args.wikipedia, worker = args.worker, language = args.language)


def command_root_delete(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper root delete",
        description = "Command `wscraper root delete` deletes default config value."
    )

    parser.add_argument("--wikipedia", action = "store_true", help = "Wikipedia name")
    parser.add_argument("--worker", action = "store_true", help = "the number of threads for working")

    args = parser.parse_args(args)

    Config.command_root_delete(wikipedia = args.wikipedia, worker = args.worker, language = args.language)


def command_set(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper set",
        description = "Command `wscraper set` sets value of parameter."
    )

    parser.add_argument("--wikipedia", help = "Wikipedia name")
    parser.add_argument("--worker", help = "the number of threads for working")
    parser.add_argument("--language", help = "Wikipedia language")

    args = parser.parse_args(args)

    Config.command_set(wikipedia = args.wikipedia, worker = args.worker, language = args.language)
