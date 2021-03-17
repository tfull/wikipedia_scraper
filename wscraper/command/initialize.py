import os

from ..base.ws_error import *
from ..base.config import *


def run(args):
    if len(args) != 0:
        raise WsError(f"Command \"initialize\" takes exactly 0 arguments.")

    Config.command_initialize()


if __name__ == '__main__':
    main()
