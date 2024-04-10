import pytest

from core.category.domain.category import Category
from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class TestSampleRepository:
    def test_save_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        category_repository = DjangoORMCategoryRepository()
        assert CategoryModel.objects.count() == 0
        category_repository.save(category)
        assert CategoryModel.objects.count() == 1

        repository_saved_category = CategoryModel.objects.first()
        assert repository_saved_category.name == category.name
        assert repository_saved_category.description == category.description

        assert CategoryModel.objects.first().name == "Movie"
        assert CategoryModel.objects.first().description == "Movie description"
