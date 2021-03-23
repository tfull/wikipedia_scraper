import re
import os
import sys
import shutil
import glob

from .constant import *
from .ws_error import *
from ..utility import *


class Config:

    template_root_config = {
        "wikipedia": None,
        "worker": 1,
        "language": None,
        "page_chunk": 10000
    }

    template_config = {
        "wikipedia": None,
        "worker": None,
        "language": None,
        "tokenizer": {},
        "model": {}
    }

    template_root_status = {
        "current": None
    }

    parameter_list = [
        "wikipedia",
        "worker",
        "language",
        "tokenizer",
        "model"
    ]

    available_languages = [
        "japanese",
        "english"
    ]

    available_algorithms = [
        "word2vec",
        "word_frequency"
    ]

    @classmethod
    def check_root_directory_exists(cls):
        if not os.path.isdir(Constant.root_directory):
            message = f"Root directory {Constant.root_directory} does not exist."
            message += " Did you run `wscraper initialize`?"
            raise WsError(message)

        if not os.path.isfile(Constant.root_config):
            raise WsError(f"Root config file {Constant.root_config} does not exist.")

        if not os.path.isfile(Constant.root_status):
            raise WsError(f"Root status file {Constant.root_status} does not exist.")

        if not os.path.isdir(Constant.wikipedia_directory):
            raise WsError(f"Wikipedia directory {Constant.wikipedia_directory} does not exist.")

        if not os.path.isdir(Constant.task_directory):
            raise WsError(f"Source directory {Constant.task_directory} does not exist.")

    @classmethod
    def command_initialize(cls):
        if os.path.isdir(Constant.root_directory):
            sys.stdout.write(f"Root directory {Constant.root_directory} already exists.\n")

            if os.path.isfile(Constant.root_config):
                sys.stdout.write(f"Root config {Constant.root_config} already exists.\n")
            else:
                FileManager.save_yaml(Constant.root_config, cls.template_root_config)
                sys.stdout.write(f"Root config {Constant.root_config} was created.\n")

            if os.path.isfile(Constant.root_status):
                sys.stdout.write(f"Root status {Constant.root_status} already exists.\n")
            else:
                FileManager.save_yaml(Constant.root_status, { "current": None })
                sys.stdout.write(f"Root status {Constant.root_status} was created.\n")

            if os.path.isdir(Constant.wikipedia_directory):
                sys.stdout.write(f"Wikipedia directory {Constant.wikipedia_directory} already exists.\n")
            else:
                os.makedirs(Constant.wikipedia_directory)
                sys.stdout.write(f"Wikipedia directory {Constant.wikipedia_directory} was created.\n")

            if os.path.isdir(Constant.task_directory):
                sys.stdout.write(f"Source directory {Constant.task_directory} already exists.\n")
            else:
                os.makedirs(Constant.task_directory)
                sys.stdout.write(f"Source directory {Constant.task_directory} was created.\n")
        else:
            os.makedirs(Constant.root_directory)
            sys.stdout.write(f"Root directory {Constant.root_directory} was created.\n")
            FileManager.save_yaml(Constant.root_config, cls.template_root_config)
            sys.stdout.write(f"Root config {Constant.root_config} was creaetd.\n")
            FileManager.save_yaml(Constant.root_status, { "current": None })
            sys.stdout.write(f"Root status {Constant.root_status} was created.\n")
            os.makedirs(Constant.wikipedia_directory)
            sys.stdout.write(f"Wikipedia directory {Constant.wikipedia_directory} was created.\n")
            os.makedirs(Constant.task_directory)
            sys.stdout.write(f"Task directory {Constant.task_directory} was created.\n")

    @classmethod
    def command_new(cls, name):
        cls.check_root_directory_exists()

        name_format = r"^[a-zA-Z0-9_\-]+$"

        if re.search(name_format, name) is None:
            raise WsError(f"Task name format shoud be composed of alphabet, number, underscore or hyphen.")

        new_directory = os.path.join(Constant.task_directory, name)

        if os.path.exists(new_directory):
            raise WsError(f"Task name {repr(name)} already exists.")

        os.makedirs(new_directory)
        sys.stdout.write(f"New task was created at {new_directory}.\n")

        path_config = os.path.join(new_directory, "config.yml")
        path_status = os.path.join(new_directory, "status.yml")

        FileManager.save_yaml(path_config, cls.template_config)
        sys.stdout.write(f"Config file was created at {path_config}.\n")
        FileManager.save_yaml(path_status, {})
        sys.stdout.write(f"Status file was created at {path_status}.\n")

    @classmethod
    def command_switch(cls, name):
        cls.check_root_directory_exists()

        if not os.path.isdir(os.path.join(Constant.task_directory, name)):
            raise WsError(f"Task name {name} does not exist.")

        path = os.path.join(Constant.root_directory, "status.yml")
        status = FileManager.load_yaml(path)
        status["current"] = name
        FileManager.save_yaml(path, status)
        sys.stdout.write(f"Task switched to {name}.\n")

    @classmethod
    def command_status(cls):
        cls.check_root_directory_exists()

        Config().print_status()

    @classmethod
    def load_root_config(cls):
        return FileManager.load_yaml(Constant.root_config)

    @classmethod
    def load_root_status(cls):
        return FileManager.load_yaml(Constant.root_status)

    @classmethod
    def load_config_by_name(cls, name):
        path = os.path.join(Constant.task_directory, name, "config.yml")

        if not os.path.isfile(path):
            raise WsError(f"Task name {name} does not exist.")

        return FileManager.load_yaml(path)

    @classmethod
    def load_status_by_name(cls, name):
        path = os.path.join(Constant.task_directory, name, "status.yml")

        if not os.path.isfile(path):
            raise WsError(f"Task name {name} does not exist.")

        return FileManager.load_yaml(path)

    def __init__(self, name = None):
        self.check_root_directory_exists()

        if name is None:
            status = FileManager.load_yaml(Constant.root_status)
            name = status["current"]
            if name is None:
                raise WsError("Current name is not set.")

        self.name = name
        self.config = self.load_config_by_name(name)
        self.root_config = self.load_root_config()
        self.status = self.load_status_by_name(name)
        self.root_status = self.load_root_status()
        self.this_directory = os.path.join(Constant.task_directory, self.name)

    def save(self):
        path = os.path.join(self.this_directory, "config.yml")
        FileManager.save_yaml(path, self.config)

    """
    def save_root(self):
        FileManager.save_yaml(Constant.root_config, self.root_config)
    """

    def print_status(self):
        # TODO strict yaml
        for key in self.parameter_list:
            data = self.config[key]

            if data is None and key in self.template_root_config:
                print(key + ":", self.root_config[key], "[default]")
            else:
                print(key + ":", data)

    def get_parameter(self, key, *, must = False):
        data = self.config

        for k in key.split("."):
            if data is not None:
                data = data.get(k)

        if data is None and key in self.template_root_config:
            data = self.root_config[key]

        if data is None and must:
            raise WsError(f"Key {key} must exist but None.")

        return data

    def set_wikipedia(self, name = None):
        wikipedia_list = []

        for path in glob.glob(os.path.join(Constant.wikipedia_directory, "*")):
            base_name = os.path.basename(path)

            if base_name[-4:] == ".xml":
                wikipedia_list.append(base_name[:-4])
            elif os.path.isdir(path):
                wikipedia_list.append(base_name)

        if len(wikipedia_list) == 0:
            raise WsError("There are no wikipedia resources.")

        if name is None:
            value_map = {}

            sys.stdout.write("Please select from these candidates.\n")

            for i, value in enumerate(wikipedia_list):
                value_map[i] = value
                sys.stdout.write(f"{i}: {value}\n")

            while name is None:
                user_input = input("Please select by number: ")

                try:
                    name = value_map[int(user_input)]
                except (ValueError, KeyError):
                    sys.stdout.write("Input value is invalid. Please try again.\n")
                except KeyboardInterrupt:
                    sys.stdout.write("Interrupted and not set.\n")
        else:
            if name not in wikipedia_list:
                raise WsError(f"No such wikipedia resource {name}.")

        self.config["wikipedia"] = name
        self.save()

    def unset_wikipedia(self):
        self.config["wikipedia"] = None
        self.save()

    def set_worker(self, number):
        if not (type(number) == int and number in range(1, 64 + 1)):
            raise WsError(f"Argument worker must satisfy 1 <= worker <= 64.")

        self.config["worker"] = number
        self.save()

    def unset_worker(self):
        self.config["worker"] = None
        self.save()

    def set_language(self, language):
        self.config["language"] = language
        self.save()

    def unset_language(self):
        self.config["language"] = None
        self.save()

    def create_model(self, name, algorithm, arguments = None):
        if name in self.config["model"]:
            raise WsError(f"Model {name} already exists.")

        if algorithm not in self.available_algorithms:
            raise WsError(f"Algorithm {algorithm} is not supported.")

        if arguments is None:
            arguments = {}

        self.config["model"][name] = {
            "algorithm": algorithm,
            "arguments": arguments
        }

        self.save()

    def delete_model(self, name):
        if name not in self.config["model"]:
            raise WsError(f"Config: Model \"{name}\" does not exist.")

        del self.config["model"][name]

        self.save()

    def delete_model_arguments(self, name, arguments = None):
        if name not in self.config["model"]:
            raise WsError(f"Model {name} does not exist.")

        if arguments is None:
            self.config["model"][name]["arguments"] = {}
            self.save()
            sys.stdout.write(f"Arguments of model {name} was made empty.\n")
            return

        for arg in arguments:
            if arg in self.config["model"][name]["arguments"]:
                del self.config["model"][name]["arguments"][arg]
                sys.stdout.write(f"Argument {arg} is deleted.\n")
            else:
                sys.stdout.write(f"No such argument {arg}. Skipped.\n")

        self.save()

    def update_model_arguments(self, name, arguments = None):
        if name not in self.config["model"]:
            raise WsError(f"Model {name} does not exist.")

        for key in arguments:
            self.config["model"][name]["arguments"][key] = arguments[key]

    def get_model(self, name = None, must = False):
        if name is not None:
            return self.get_parameter(f"model.{name}", must = must)
        else:
            return self.get_parameter("model", must = must)

    def model_name_exists(self, name):
        item = self.get_parameter("model", must = True)
        return name in item

    def confirm_model_names_exist(self, model_name_list):
        no_existing_list = []

        item = self.get_parameter("model", must = True)

        for model_name in model_name_list:
            if model_name not in item:
                no_existing_list.append()

    def set_tokenizer(self, name, arguments):
        self.config["tokenizer"] = {
            "name": name,
            "arguments": arguments
        }

        self.save()

    def unset_tokenizer(self):
        self.config["tokenizer"] = {}
        self.save()

    def get_tokenizer(self, must):
        return self.get_parameter("tokenizer", must = must)

    def get_wikipedia_xml(self, *, must = True):
        wikipedia_name = self.get_parameter("wikipedia", must = True)
        wikipedia_xml = os.path.join(Constant.wikipedia_directory, wikipedia_name + ".xml")

        if must and not os.path.isfile(wikipedia_xml):
            raise WsError(f"No such file {wikipedia_xml}.")

        return wikipedia_xml

    def get_wikipedia_xml_directory(self, *, must = True, optional = False):
        wikipedia_name = self.get_parameter("wikipedia", must = True)
        wikipedia_xml_directory = os.path.join(Constant.wikipedia_directory, wikipedia_name)

        if must and not os.path.isdir(wikipedia_xml_directory):
            raise WsError(f"No such directory {wikipedia_xml_directory}.")

        return wikipedia_xml_directory

    def make_workspace(self, workspace_name, exist_ok = True):
        target_directory = os.path.join(self.this_directory, "workspace", workspace_name)
        os.makedirs(target_directory, exist_ok = exist_ok)
        return target_directory

    def make_model_directory(self, exist_ok = True):
        model_directory = os.path.join(self.this_directory, "model")
        os.makedirs(model_directory, exist_ok = exist_ok)
        return model_directory
