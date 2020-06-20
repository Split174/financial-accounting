"""
this module contains classes describing relationships

classes:
Account - describes the ratio account
Category - describes the ratio сategory
LevelCategory - describes the ratio levelcategory
Operation - describes the ratio operation
"""
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AccountModel(Base):
    """
    The class describes the relationship account
    :param - base class that all related classes inherit from
    method:
    as_dict - provides the ability to receive data relationship account
    :return - data dictionary
    """
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text, unique=True)
    password = Column(Text)

    def as_dict(self):
        account = {c.name: getattr(self, c.name)
                   for c in self.__table__.columns}
        account.pop('password')
        return account


class CategoryModel(Base):
    """
    The class describes the relationship category
    :param - base class that all related classes inherit from
    method:
    as_dict - provides the ability to receive data relationship category
    :return - data dictionary
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    user_id = Column(Integer, ForeignKey('account.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class LevelCategoryModel(Base):
    """
    The class describes the relationship levelcategory
    :param - base class that all related classes inherit from
    method:
    as_dict - provides the ability to receive data relationship levelcategory
    :return - data dictionary
    """
    __tablename__ = 'levelcategory'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('category.id'))
    children_id = Column(Integer, ForeignKey('category.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class OperationModel(Base):
    """
    The class describes the relationship operation
    :param - base class that all related classes inherit from
    method:
    as_dict - provides the ability to receive data relationship operation
    :return - data dictionary
    """
    __tablename__ = 'operation'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    description = Column(Text)
    datetime = Column(Integer)
    type_operation = Column(Text)
    user_id = Column(Integer, ForeignKey('account.id'))
    category_id = Column(Integer, ForeignKey('category.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

