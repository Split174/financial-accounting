from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Operation:
    type_operation: str
    amount: int
    category_id: Optional[int]
    datetime: Optional[date]
    description: Optional[str]


@dataclass
class GetOperation(Operation):
    id: int
    user_id: int


@dataclass
class UpdateOperation:
    type_operation: Optional[str]
    amount: Optional[int]
    category_id: Optional[int]
    datetime: Optional[date]
    description: Optional[str]
