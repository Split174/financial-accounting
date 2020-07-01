"""
the module implements a service for working with categories
:classes:
CategoryServiceError - base class of exceptions for the service
CategoryService - implement service category
"""
from exceptions import ServiceError
from models import CategoryModel, LevelCategoryModel
from entities.category import Category, CategoryTree
from sqlalchemy import and_, func
from typing import Optional, List, NoReturn


class CategoryServiceError(ServiceError):
    service = 'category'


class CategoryAlredyExist(CategoryServiceError):
    pass


class CategoryIdDoesNotExist(CategoryServiceError):
    pass


class CategoryParentDoesNotExist(CategoryServiceError):
    pass


class CategoryService:
    def __init__(self, session, user_id):
        self.session = session
        self.user_id = user_id

    def add_category(self, category: Category) -> Category:
        """
        Add new category
        :param category: Category(dataclass)
        :return: new category
        """
        category.name = category.name.lower()
        if category.parent_id is not None and self.__get_category_model_by_id(
                category.parent_id) is None:
            raise CategoryIdDoesNotExist()

        if self.__get_category_model_by_name(category.name) is not None:
            raise CategoryAlredyExist()

        new_category = CategoryModel(name=category.name, user_id=self.user_id)
        self.session.add(new_category)
        self.session.commit()

        new_level_category = LevelCategoryModel(parent_id=category.parent_id,
                                                children_id=new_category.id)
        self.session.add(new_level_category)
        self.session.commit()
        return Category(id=new_category.id, name=new_category.name,
                        parent_id=category.parent_id)

    def change_category(self, category: Category) -> Category:
        """
        Category change
        :param category: Category
        :return: modified category
        """
        if category.parent_id == 0:
            category.parent_id = None
        if self.__get_category_model_by_id(category.id) is None:
            raise CategoryIdDoesNotExist()

        if self.__get_category_model_by_name(category.name) is not None:
            raise CategoryAlredyExist()
        if (category.parent_id != -1 and category.parent_id is not None
                and self.__get_category_model_by_id(
                    category.parent_id) is None):
            raise CategoryParentDoesNotExist()

        if category.name is not None:
            category.name = category.name.lower()
            self.__change_category_name(category.id, category.name)
        if category.parent_id != -1:
            self.__change_category_parent_id(category.id, category.parent_id)
        parent = (
            self.session.query(LevelCategoryModel)
                .filter(LevelCategoryModel.children_id == category.id).first()
        )
        category_row = self.__get_category_model_by_id(category.id)
        if parent is not None:
            parent = parent.parent_id
        return Category(name=category_row.name, id=category_row.id,
                        parent_id=parent)

    def delete_category(self, category_id: int) -> NoReturn:
        """
        category removal
        :param category_id: int
        """
        if self.__get_category_model_by_id(category_id) is None:
            raise CategoryIdDoesNotExist()
        tree = self.__get_category_tree(category_id)
        self.__delete_category_tree(tree)

    def get_all_tree(self) -> List[CategoryTree]:
        """
        Getting all category trees
        :return: List[CategoryTree]
        """
        top_level_category: List[int] = self.__get_top_level_category_ids()
        res: List[CategoryTree] = []
        for category_id in top_level_category:
            res.append(self.__get_category_tree(category_id))
        return res

    def get_category_tree(self, category_id: int) -> CategoryTree:
        """
        Getting tree categories
        :param category_id: int
        :return: CategoryTree
        """
        if self.__get_category_model_by_id(category_id) is None:
            raise CategoryIdDoesNotExist()
        return self.__get_category_tree(category_id)

    def __get_top_level_category_ids(self) -> List[int]:
        """
        Getting categories id without a parent
        :return: List[int]
        """
        categories = (self.session.query(CategoryModel)
                      .join(LevelCategoryModel, (
            and_(CategoryModel.id == LevelCategoryModel.children_id)))
                      .filter(and_(CategoryModel.user_id == self.user_id,
                                   LevelCategoryModel.parent_id.is_(
                                       None))).all())
        return [cat.id for cat in categories]

    def __get_category_tree(self, category_id) -> Optional[CategoryTree]:
        """
        Recursively retrieving category tree
        """
        children = self.session.query(LevelCategoryModel).filter(
            LevelCategoryModel.parent_id == category_id).all()
        tree = CategoryTree(
            name=self.__get_category_model_by_id(category_id).name,
            id=category_id, children=[])
        for child in children:
            tree.children.append(self.__get_category_tree(child.children_id))
        if len(children) == 0:
            tree.children = None
        return tree

    def __delete_category_tree(self, tree: Optional[CategoryTree]) -> NoReturn:
        """
        Recursively delete category tree
        """
        if tree is None:
            return
        self.session.execute("PRAGMA foreign_keys=ON;")
        (self.session.query(CategoryModel)
         .filter(and_(
            CategoryModel.user_id == self.user_id,
            CategoryModel.id == tree.id))
         .delete())
        self.session.commit()
        if tree.children is not None:
            for child in tree.children:
                self.__delete_category_tree(child)

    def __get_category_model_by_id(self, category_id: int) -> Optional[CategoryModel]:
        """get category model by ID"""
        return self.session.query(CategoryModel).filter(
            and_(CategoryModel.id == category_id,
                 CategoryModel.user_id == self.user_id)).first()

    def __get_category_model_by_name(self, name: str) -> Optional[CategoryModel]:
        """get category model by NAME"""
        return self.session.query(CategoryModel).filter(
            and_(CategoryModel.name == name,
                 CategoryModel.user_id == self.user_id)).first()

    def __change_category_name(self, category_id: int,
                               new_name: str) -> CategoryModel:
        """
        change category name
        :param category_id: id category
        :param new_name: name
        :return: modified category
        """
        category = self.session.query(CategoryModel).filter(
            and_(CategoryModel.id == category_id,
                 CategoryModel.user_id == self.user_id)).first()
        category.name = new_name
        self.session.commit()
        return category

    def __change_category_parent_id(self, child_id: int,
                                    new_parent_id: int) -> LevelCategoryModel:
        """
        change LevelCategory parent_id
        :param child_id: child id
        :param new_parent_id: parent_id
        :return: modified levelcategorymodel
        """
        changed_level = (self.session.query(LevelCategoryModel)
                         .filter(
            LevelCategoryModel.children_id == child_id).first())
        changed_level.parent_id = new_parent_id
        self.session.commit()
        return changed_level
