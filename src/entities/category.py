from dataclasses import dataclass
from typing import Optional, List, Any


@dataclass
class CategoryBase:
    name: str


@dataclass
class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None
    id: Optional[int] = None
    parent_name: Optional[str] = None


@dataclass
class CategoryTree(CategoryBase):
    id: int
    children: Optional[List[Any]] # TODO лучше избавиться от Any

