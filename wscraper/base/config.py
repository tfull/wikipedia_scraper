import re

from .constant import *
from .ws_error import *
from ..utility import *


class Config:

    root_template = {
        "wikipedia_xml": None,
        "worker": 1,
        "language": None
    }

    template = {
        "wikipedia_xml": None,
        "worker": None,
        "language": None,
        "tokenizer": {}, # atom
        "model": {} # name and model
    }

    parameter_list = [
        "wikipedia_xml",
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
            raise WsError(f"Root directory \"{Constant.root_directory}\" does not exist.")

    @classmethod
    def command_initialize(cls):
        if os.path.isfile(Constant.root_directory):
            raise WsError(f"Root directory \"{Constant.root_directory}\" already exists as a file.")

        os.makedirs(Constant.root_directory, exist_ok = True)

        if not os.path.isfile(Constant.root_config):
            FileManager.save_yaml(Constant.root_config, cls.root_template)
            FileManager.save_yaml(Constant.root_status, { "current": None })

    @classmethod
    def command_new(cls, name):
        cls.check_root_directory_exists()

        name_format = r"^[a-zA-Z0-9_\-]+$"

        if re.search(name_format, name) is None:
            raise WsError(f"Command \"new\": Name format shoud be \"{name_format}\".")

        new_directory = os.path.join(Constant.root_directory, name)

        if os.path.exists(new_directory):
            raise WsError(f"Command \"new\": Name \"{name}\" already exists.")

        os.makedirs(new_directory)

        FileManager.save_yaml(os.path.join(new_directory, "config.yml"), cls.template)
        FileManager.save_yaml(os.path.join(new_directory, "status.yml"), {})

    @classmethod
    def command_switch(cls, name):
        cls.check_root_directory_exists()

        if not os.path.isdir(os.path.join(Constant.root_directory, name)):
            raise WsError(f"Command \"switch\": Name {name} does not exist.")

        path = os.path.join(Constant.root_directory, "status.yml")

        status = FileManager.load_yaml(path)
        status["current"] = name
        FileManager.save_yaml(path, status)

    @classmethod
    def load_root_config(cls):
        if not os.path.isfile(Constant.root_config):
            raise WsError(f"Config: Root config \"{Constant.root_config} does not exist.\"")

        return FileManager.load_yaml(Constant.root_config)

    @classmethod
    def load_config_by_name(cls, name):
        path = os.path.join(Constant.root_directory, name, "config.yml")

        if not os.path.isfile(path):
            raise WsError(f"Config: Name \"{name}\" does not exist.")

        return FileManager.load_yaml(path)

    @classmethod
    def load_status_by_name(cls, name):
        path = os.path.join(Constant.root_directory, name, "status.yml")

        if not os.path.isfile(path):
            raise WsError(f"Config: Name \"{name}\" does not exist.")

        return FileManager.load_yaml(path)

    def __init__(self, name = None):
        self.check_root_directory_exists()

        if name is None:
            status = FileManager.load_yaml(Constant.root_status)
            name = status["current"]
            if name is None:
                raise WsError("Config: Current name is not set.")

        self.name = name
        self.config = self.load_config_by_name(name)

        for key, value in self.load_root_config().items():
            if key not in self.config or self.config[key] is None:
                self.config[key] = value

        self.status = self.load_status_by_name(name)

    def save(self):
        path = os.path.join(Constant.root_directory, self.name, "config.yml")
        FileManager.save_yaml(path, self.config)

    def print_parameters(self):
        for param in self.parameter_list:
            print(param + ":", self.config[param])

    def get_parameter(self, key, *, must = False):
        data = self.config

        for k in key.split("."):
            if data is not None:
                data = data.get(k)

        if data is None and must:
            raise WsError(f"Config: Key \"{key}\" must exist but None.")

        return data

    def set_wikipedia_xml(self, name):
        self.config["wikipedia_xml"] = name
        self.save()

    def delete_wikipedia_xml(self):
        self.config["wikipedia_xml"] = None
        self.save()

    def set_worker(self, number):
        if not (type(number) == int and number in range(1, 64 + 1)):
            raise WsError(f"Config: Argument worker must satisfy 1 <= worker <= 64")

        self.config["worker"] = number
        self.save()

    def delete_worker(self):
        self.config["worker"] = None
        self.save()

    def set_language(self, language):
        self.config["language"] = language
        self.save()

    def delete_language(self):
        self.config["language"] = None
        self.save()

    def model_new(self, name, algorithm, arguments = None):
        if name in self.config["model"]:
            raise WsError(f"Config: Model \"{name}\" already exists.")

        if algorithm not in self.available_algorithms:
            raise WsError(f"Config: Algorithm \"{algorithm}\" is not supported.")

        if arguments is None:
            arguments = {}

        self.config["model"][name] = {
            "algorithm": algorithm,
            "arguments": arguments
        }

        self.save()

    def model_delete(self, name):
        if name not in self.config["model"]:
            raise WsError(f"Config: Model \"{name}\" does not exist.")

        del self.config["model"][name]

        self.save()

    def set_tokenizer(self, name, arguments):
        self.config["tokenizer"] = {
            "name": name,
            "arguments": arguments
        }

        self.save()

    def delete_tokenizer(self):
        self.config["tokenizer"] = {}
        self.save()
