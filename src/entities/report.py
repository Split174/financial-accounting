"""
the module contains dataclasses
:classes:
Report - dataclass from input data
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict
from decimal import Decimal


@dataclass
class Report:
    """
    dataclass from input data
    """
    start_date: Optional[datetime]
    finish_date: Optional[datetime]
    category_name: Optional[str]
    page: int
    page_size: int
    ready_date: [str]




@dataclass
class ReportReturn:

    amount: Decimal
    description: str
    datetime: datetime
    category: List['Category']
    result_sum: Decimal


@dataclass
class Category:
    id: Dict[int]
    name: Dict[str]
