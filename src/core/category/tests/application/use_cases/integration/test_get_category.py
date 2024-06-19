import uuid

import pytest

from src.core.category.application.exceptions import CategoryDoesNotExistsException
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)


class TestGetCategory:
    def test_get_category_by_id(self):
        category_film = Category(
            name="Movie",
            description="Some description",
        )
        category_serie = Category(
            name="Serie",
            description="Some description",
        )
        repository = InMemoryCategoryRepository([category_film, category_serie])
        use_case = GetCategory(repository=repository)

        request = GetCategoryRequest(id=category_film.id)

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category_film.id,
            name=category_film.name,
            description=category_film.description,
            is_active=category_film.is_active,
        )
        assert response.id == category_film.id
        assert response.name == category_film.name
        assert response.description == category_film.description
        assert response.is_active == category_film.is_active

    def test_when_category_not_exist_when_raise_exception(self):
        category_film = Category(
            name="Movie",
            description="Some description",
        )
        category_serie = Category(
            name="Serie",
            description="Some description",
        )
        repository = InMemoryCategoryRepository([category_film, category_serie])
        use_case = GetCategory(repository=repository)
        not_found_id = uuid.uuid4()
        request = GetCategoryRequest(id=not_found_id)

        with pytest.raises(CategoryDoesNotExistsException) as error:
            use_case.execute(request)

        assert error.type == CategoryDoesNotExistsException
        assert str(error.value) == f"Category id {not_found_id} does not exists"
