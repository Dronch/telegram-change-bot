from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from types import ModuleType

from .models import meta, ExchangeRateModel, Cache


class Database(object):

    @classmethod
    def from_config(cls, config: ModuleType):
        connection_query = getattr(config, 'DATABASE_SQLALCHEMY_URL', 'sqlite:////app.db')
        return cls(connection_query)

    def __init__(self, connection_query):
        self.engine = create_engine(connection_query)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        meta.create_all(self.engine)
