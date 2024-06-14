import unittest.mock

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from core.config import Config
from sqlalchemy.orm.session import sessionmaker


cfg: Config = Config()


class Base(DeclarativeBase):
    pass


class DBConnection:

    @staticmethod
    def connect_db():
        test_mode = cfg.MODE_TEST
        env: str = cfg.ENV
        if test_mode == 'develop':
            database_url: str = cfg.get_environment_config(env)
            engine = create_engine(database_url, echo=True)
            session = sessionmaker(bind=engine)
            return session()
        else:
            engine = create_engine(cfg.get_environment_config(env))
            session = sessionmaker(bind=engine, autoflush=False)
            mock_session = unittest.mock.Mock(spec=session)
            return mock_session


