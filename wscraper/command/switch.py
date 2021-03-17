import os
import re

from ..base.config import *
from ..base.constant import *
from ..base.ws_error import *


def run(args):
    if len(args) != 1:
        raise WsError(f"[command] Switch: It takes exactly 1 argument.")

    Config.command_switch(args[0])
