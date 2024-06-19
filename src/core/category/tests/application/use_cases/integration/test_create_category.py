from uuid import UUID

import pytest

from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
)
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)


class TestCreatecategory:
    def test_create_category_with_vallid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="Movie",
            description="Some description",
            is_active=True,
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        assert repository.categories[0].id == response.id

        persited_category = repository.categories[0]
        assert persited_category.name == "Movie"
        assert persited_category.description == "Some description"
        assert persited_category.is_active is True

    def test_category_with_invalid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(
            name="",
        )
        with pytest.raises(InvalidCategoryData, match="Name cannot be empty") as error:
            use_case.execute(request=request)

        assert error.type == InvalidCategoryData
        assert str(error.value) == "Name cannot be empty"
        assert len(repository.categories) == 0
