from unittest.mock import MagicMock, create_autospec

import pytest

from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestGetCategory:
    def test_return_found_category(self):
        category = Category(
            name="Movie",
            description="Some description",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(
            id=category.id,
        )

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

        # assert response.id is not None
        # assert isinstance(response, GetCategoryResponse)
        # assert isinstance(response.id, UUID)
        # assert mock_repository.save.called is True

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
