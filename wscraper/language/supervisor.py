# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.


class Supervisor:

    @classmethod
    def get_language_class(cls, name):
        if name == "ja":
            from .japanese import Japanese
            return Japanese
        else:
            from .english import English
            return English
