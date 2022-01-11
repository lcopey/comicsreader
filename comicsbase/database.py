import sqlalchemy as db
import pandas as pd
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine()
Base = declarative_base()


class AsDict:
    __attr__ = []

    def as_dict(self):
        return {key: self.__getattribute__(key) for key in self.__attr__}

    @classmethod
    def from_series(cls, x: pd.Series):
        return cls(**x[cls.__attr__].to_dict())

    def __repr__(self):
        return self.as_dict().__str__()


class Serie(Base, AsDict):
    __tablename__ = 'series'
    __attr__ = ['id', 'serie']
    id = Column(Integer, primary_key=True)
    serie = Column(String)
    books = relationship('Book', backref=backref('series'))


class Book(Base, AsDict):
    __tablename__ = 'books'
    __attr__ = ['id', 'serie_id', 'name', 'dates', 'volumes']
    id = Column(Integer, primary_key=True)
    serie_id = Column(Integer, ForeignKey('series.id'))
    name = Column(String)
    dates = Column(String)
    volumes = Column(String)


series = Table('series', Base.metadata, autoload=True, autoload_with=engine)
books = Table('books', Base.metadata, autoload=True, autoload_with=engine)
