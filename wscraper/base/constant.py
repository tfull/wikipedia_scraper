import os


class Constant:

    root_directory = os.path.join(os.environ["HOME"], ".wscraper")

    root_config = os.path.join(root_directory, "config.yml")
    root_status = os.path.join(root_directory, "status.yml")
