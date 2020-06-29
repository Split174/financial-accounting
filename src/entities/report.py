"""
the module contains dataclasses
:classes:
Report - dataclass from input data
ReportGet - dataclass for list with total
ReportOperation - date class for list items
CategoryOperation - dataclass for dictionary items
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
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
class ReportGet:
    """
    dataclass for list with total
    """
    result_income: Optional[Decimal]
    result_sum: Optional[Decimal]
    operation: List["ReportOperation"]


@dataclass
class ReportOperation:
    """
    dataclass for list items
    """
    amount: Decimal
    description: str
    datetime: datetime
    category: List["CategoryOperation"]


@dataclass
class CategoryOperation:
    """
    dataclass for dictionary items
    """
    id: int
    name: str