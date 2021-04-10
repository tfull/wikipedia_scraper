# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseHandler:

    @classmethod
    def command_database_save(cls):
        this = cls.load()

        # TODO save code
        pass

    @classmethod
    def load(cls, task_name = None):
        config = Config(task_name)
        parameters = config.get_parameter("database", must = True)
        return cls(parameters)

    def __init__(self, parameters):
        dialect = parameters.get("dialect")
        driver = parameters.get("driver") or "default"
        user = parameters.get("user")
        password = parameters.get("password")
        host = parameters.get("host")
        port = parameters.get("port")
        database = parameters.get("database")
        charset = parameters.get("charset") or "utf8"

        self.uri = "{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(
            dialect = dialect,
            driver = driver,
            user = user,
            password = password,
            host = host,
            port = port,
            database = database,
            charset = charset
        )

        self.engine = create_engine(self.uri)
        self.session_class = sessionmaker(self.engine)

    def get_session(self):
        return self.session_class()

    @contextmanager
    def session_scope(self):
        session = self.session_class()
        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
