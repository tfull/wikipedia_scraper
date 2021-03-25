# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.


from ..base import *
from .w_scraper_algorithm_error import *


class Algorithm:

    @classmethod
    def command_build(cls, task_name = None, model_name_list = None, reset = False):
        from ..base import Config

        config = Config(task_name)

        config_model_names = config.get_model(must = True).keys()

        if model_name_list is None or len(model_name_list) == 0:
            model_name_list = config_model_names
        else:
            no_such_model_name_list = []

            for model_name in model_name_list:
                if model_name not in config.get_model.keys():
                    no_such_model_name_list.append(model)

            if len(no_such_model_name_list) > 0:
                raise WScraperConfigError(f"No such model name {', '.join(no_such_model_name_list)}.")

        sys.stdout.write(f"Building model {', '.join(model_name_list)}...\n")

        for model_name in model_name_list:
            model_item = config.get_parameter(f"model.{model_name}.")
            cls.build_sub(config, model_name, reset)

    @classmethod
    def build_sub(cls, config, model_name, reset):
        algorithm = config.get_parameter(f"model.{model_name}.{'algorithm'}")

        if algorithm == "word2vec":
            from .word_2_vec_handler import Word2VecHandler
            Word2VecHandler.build(task_name = None, model_name = model_name, config = config, reset = reset)
        elif algorithm == "word_frequency":
            from .word_frequency import WordFrequency
            WordFrequency.build(task_name = None, model_name = model_name, config = config, reset = reset)
        else:
            raise WScraperAlgorithmError(f"Algorithm {algorithm} is not implemented.\n")
