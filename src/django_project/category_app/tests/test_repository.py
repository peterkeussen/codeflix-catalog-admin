import pytest

from core.category.domain.category import Category
from src.django_project.category_app.models import Category as CategoryORM
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category() -> Category:
    category_repository = DjangoORMCategoryRepository()
    category = Category(
        name="Movie",
        description="Movie description",
    )
    category_repository.save(category)
    return category


@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        category_repository = DjangoORMCategoryRepository()
        assert CategoryORM.objects.count() == 0
        category_repository.save(category)
        assert CategoryORM.objects.count() == 1

        repository_saved_category = CategoryORM.objects.first()
        assert repository_saved_category.name == category.name
        assert repository_saved_category.description == category.description

        assert CategoryORM.objects.first().name == "Movie"
        assert CategoryORM.objects.first().description == "Movie description"


@pytest.mark.django_db
class TestUpdate:
    def test_updates_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        category_repository = DjangoORMCategoryRepository()
        assert CategoryORM.objects.count() == 0
        category_repository.save(category)
        assert CategoryORM.objects.count() == 1
        category.update("Movie updated", "Movie description updated")

        category_repository.update(category)
        assert CategoryORM.objects.count() == 1
        repository_saved_category = CategoryORM.objects.first()
        assert repository_saved_category.name == "Movie updated"
        assert repository_saved_category.description == "Movie description updated"
        assert repository_saved_category.is_active == True


@pytest.mark.django_db
class TestList:
    def test_list_all_categories_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        category_repository = DjangoORMCategoryRepository()
        assert CategoryORM.objects.count() == 0
        category_repository.save(category)
        assert CategoryORM.objects.count() == 1
        assert len(category_repository.list()) == 1

        category_orm = CategoryORM.objects.first()
        assert category_orm.id == category.id
        assert category_orm.name == category.name
        assert category_orm.description == category.description

        # print(category_repository.list())
        # print([category])
        # assert category_repository.list() == [category]


@pytest.mark.django_db
class TestGet:
    def test_get_by_id(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        category_repository = DjangoORMCategoryRepository()
        assert CategoryORM.objects.count() == 0
        category_repository.save(category)
        assert CategoryORM.objects.count() == 1
        category_orm = CategoryORM.objects.get(id=category.id)
        assert category_orm.id == category.id
        assert category_orm.name == category.name
        assert category_orm.description == category.description


@pytest.mark.django_db
class TestDelete:
    def test_delete_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        category_repository = DjangoORMCategoryRepository()
        assert CategoryORM.objects.count() == 0
        category_repository.save(category)
        assert CategoryORM.objects.count() == 1
        category_repository.delete(category.id)
        assert CategoryORM.objects.count() == 0


@pytest.mark.django_db
class TestGetByName:
    def test_get_by_name(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        category_repository = DjangoORMCategoryRepository()
        assert CategoryORM.objects.count() == 0
        category_repository.save(category)
        assert CategoryORM.objects.count() == 1
        category_orm = CategoryORM.objects.get(name=category.name)
        assert category_orm.id == category.id
        assert category_orm.name == category.name
        assert category_orm.description == category.description
