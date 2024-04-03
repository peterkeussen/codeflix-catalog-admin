import uuid

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)


class TestSaveCategory:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category_film = Category(name="Movie")
        repository.save(category_film)
        category_serie = Category(name="Serie")
        repository.save(category_serie)

        assert len(repository.categories) == 2
        assert repository.categories[0] == category_film


class TestGetByIdCategory:
    def test_can_get_by_id(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="Movie")
        repository.save(category)

        assert repository.get_by_id(category.id) == category

    def test_get_by_id_raises_exception(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="Movie")
        repository.save(category)

        assert repository.get_by_id(uuid.uuid4()) is None


class TestDeleteCategory:
    def test_can_delete(self):
        category_film = Category(name="Movie")
        category_serie = Category(name="Serie")
        repository = InMemoryCategoryRepository([category_film, category_serie])

        category_film2 = Category(name="Movie")
        repository.save(category_film2)
        category_serie2 = Category(name="Serie")
        repository.save(category_serie2)

        repository.delete(category_film.id)

        assert len(repository.categories) == 3
        assert repository.categories[0] == category_serie
