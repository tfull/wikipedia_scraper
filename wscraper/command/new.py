import os
import re

from ..base.config import *
from ..base.constant import *


def run(args):
    if len(args) != 1:
        raise WsError(f"Command \"new\" takes exactly 1 argument.")

    Config.command_new(args[0])
