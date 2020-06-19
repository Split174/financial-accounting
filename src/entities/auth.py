"""
this module allows you to convert
the transmitted authorization data into a dataclass
:classes:
Auth - converts data into a dataclass
"""
from dataclasses import dataclass


@dataclass
class Auth:
    """
    converts registration data into a dataclass
    """
    email: str
    password: str
