"""
The module implements category entities
"""
from dataclasses import dataclass
from typing import Optional, List, Any


@dataclass
class CategoryBase:
    name: str


@dataclass
class Category(CategoryBase):
    id: Optional[int] = None
    parent_id: Optional[int] = None


@dataclass
class CategoryTree(CategoryBase):
    id: int
    children: Optional[List['CategoryTree']]

