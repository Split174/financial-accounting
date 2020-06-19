"""
this module allows you to convert
the transmitted and returned registration data into a data class
:classes:
BaseUser - parent class to inherit
User - converts return data into a dateclass
UserCreate - converts insert data into a dateclass
"""
from dataclasses import dataclass


@dataclass
class BaseUser:
    """
    parent class to inherit
    """
    email: str
    first_name: str
    last_name: str


@dataclass
class User(BaseUser):
    """
    class for converting returned data
    """
    id: int


@dataclass
class UserCreate(BaseUser):
    """
    class for converting insert data
    """
    password: str
