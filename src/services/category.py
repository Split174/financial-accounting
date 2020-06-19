from exceptions import ServiceError
from models import CategoryModel, LevelCategoryModel
from entities.category import CategoryCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_


class CategoryServiceError(ServiceError):
    service = 'category'


class CategoryAlredyExist(CategoryServiceError):
    pass


class CategoryParentIdDoesNotExist(CategoryServiceError):
    pass


class CategoryService:
    def __init__(self, session, user_id):
        self.session = session
        self.user_id = user_id

    def add_category(self, category: CategoryCreate) -> CategoryCreate:
        if category.parent_id is not None and self.__get_category_model_by_id(category.parent_id) is None:
            raise CategoryParentIdDoesNotExist()

        if self.__get_category_name_by_id(category.name) is not None:
            raise CategoryAlredyExist()

        new_category = CategoryModel(name=category.name, user_id=self.user_id)
        self.session.add(new_category)
        self.session.comit()

        parent_name = None
        if category.parent_id is not None:
            new_level_category = LevelCategoryModel(parent_id=category.parent_id, children_id=new_category.id)
            self.session.add(new_level_category)
            self.session.comit()
            parent_name = self.__get_category_name_by_id(category.parent_id, self.user_id)
        return CategoryCreate(id=new_category.id, name=new_category.name, parent_name=parent_name)

    def __get_category_model_by_id(self, category_id: int) -> bool:
        """Получить модель категории по ID"""
        return self.session.query(CategoryModel).filter(and_(CategoryModel.id == category_id,
                                                             CategoryModel.user_id == self.user_id)).first()

    def __get_category_model_by_name(self, name: str) -> object:
        """Получить модель категории по имени"""
        return self.session.query(CategoryModel).filter(and_(CategoryModel.name == name,
                                                             CategoryModel.user_id == self.user_id)).first()

    def __get_category_name_by_id(self, category_id: int, user_id: int):
        category_row = self.session.query(CategoryModel).filter(and_(CategoryModel.id == category_id,
                                                                     CategoryModel.user_id == user_id)).first()
        return category_row.name if category_row is not None else None
