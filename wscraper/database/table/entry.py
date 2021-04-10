# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text

from .base import *


class Entry(Base):

    id = Column(Integer, primary_key = True)
    title = Column(String(255), index = True)
    mediawiki = Column(Text)
    document = Column(Text)
