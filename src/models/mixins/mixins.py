from sqlalchemy import Column, TIMESTAMP
from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr


class TableMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_on = Column(TIMESTAMP(), default=datetime.now)
    updated_on = Column(TIMESTAMP(), default=datetime.now, onupdate=datetime.now)
    deleted_on = Column(TIMESTAMP(), default=None)
