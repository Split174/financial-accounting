"""
the module contains a basic scheme
"""
from marshmallow import Schema, post_load


class BaseSchema(Schema):
    """
    class for inheritance and and transfers to dataclass
    :methods:
    make_object - convert to dataclass
    """
    __entity_class__ = None

    @post_load
    def make_object(self, data, **kwargs):
        """
        convert to dataclass
        :param data: convert data
        :return: dataclass
        """
        return self.__entity_class__(**data)
