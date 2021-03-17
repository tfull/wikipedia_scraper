import re

from .constant import *
from .ws_error import *
from ..utility import *


class Config:

    root_template = {
        "wikipedia_xml": None,
        "worker": 1
    }

    template = {
        "wikipedia_xml": None
    }

    parameter_list = [
        ("wikipedia_xml", 1),
        ("worker", 2)
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

        self.config = self.load_config_by_name(name)

        for key, value in self.load_root_config().items():
            if key not in self.config or self.config[key] is None:
                self.config[key] = value

        self.status = self.load_status_by_name(name)

    def print_parameters(self):
        print(self.config)

    def get_parameter(self, key):
        if key not in self.config:
            raise WsError(f"Config: Key \"{key}\" does not exist.")

        return self.config[key]

    def set_parameter(self, key, value):
        pass
