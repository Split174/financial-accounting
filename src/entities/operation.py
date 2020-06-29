"""
module with data classes for data conversion
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass
class Operation:
    """
    dataclass for input data conversion
    """
    type_operation: str
    amount: Decimal
    category_id: Optional[int]
    datetime: Optional[datetime]
    description: Optional[str]


@dataclass
class GetOperation(Operation):
    """
    dataclass for get data conversion
    """
    id: int
    user_id: int


@dataclass
class UpdateOperation:
    """
    dataclass for input data conversion
    """
    type_operation: Optional[str]
    amount: Optional[Decimal]
    category_id: Optional[int]
    datetime: Optional[datetime]
    description: Optional[str]
