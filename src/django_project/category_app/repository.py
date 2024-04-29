from typing import Optional, Union
from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel = CategoryModel) -> None:  # type: ignore
        self.category_model = category_model

    def save(self, category: Category) -> None:
        category_orm = CategoryModelMapper.to_model(category)
        category_orm.save()

    def update(self, category: Category) -> None:
        self.category_model.objects.filter(id=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()

    def list(self) -> list[Category]:
        categories = self.category_model.objects.all()
        return [CategoryModelMapper.to_entity(category) for category in categories]
        # return [
        #     Category(
        #         id=category.id,
        #         name=category.name,
        #         description=category.description,
        #         is_active=category.is_active,
        #     )
        #     for category in categories
        # ]

    def get_by_id(self, category_id: UUID) -> Category | None:
        try:
            category = self.category_model.objects.get(id=category_id)
            return CategoryModelMapper.to_entity(category)
        except self.category_model.DoesNotExist:
            return None

    def get_by_name(self, name: str) -> Union[Category, None]:
        try:
            category = self.category_model.objects.get(name=name)
            return CategoryModelMapper.to_entity(category)
        except self.category_model.DoesNotExist:
            return None


class CategoryModelMapper:
    @staticmethod
    def to_model(category: Category) -> CategoryModel:
        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    @staticmethod
    def to_entity(category_model: CategoryModel) -> Category:
        return Category(
            id=category_model.id,
            name=category_model.name,
            description=category_model.description,
            is_active=category_model.is_active,
        )
