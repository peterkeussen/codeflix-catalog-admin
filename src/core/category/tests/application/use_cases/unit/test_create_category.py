from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
)
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)


class TestCreatecategoryInRepository:
    def test_create_category_with_vallid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name="Movie",
            description="Some description",
            is_active=True,
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True

    def test_category_with_invalid_data(self):
        # with pytest.raises(ValueError, match="Name cannot be empty"): # Transpasa a camada de domínio
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name="",
        )
        with pytest.raises(InvalidCategoryData, match="Name cannot be empty") as error:
            use_case.execute(request=request)

        assert error.type == InvalidCategoryData
        assert str(error.value) == "Name cannot be empty"
        assert mock_repository.save.called is False


class TestCreatecategoryInMemoryRepository:
    def test_create_category_with_vallid_data(self):
        mock_repository = MagicMock(InMemoryCategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name="Movie",
            description="Some description",
            is_active=True,
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True

    def test_category_with_invalid_data(self):
        # with pytest.raises(ValueError, match="Name cannot be empty"): # Transpasa a camada de domínio
        mock_repository = MagicMock(InMemoryCategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name="",
        )
        with pytest.raises(InvalidCategoryData, match="Name cannot be empty") as error:
            category_id = use_case.execute(request=request)

        assert error.type == InvalidCategoryData
        assert str(error.value) == "Name cannot be empty"
        assert mock_repository.save.called is False
