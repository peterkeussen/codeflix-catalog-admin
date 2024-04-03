import uuid
from unittest.mock import MagicMock, create_autospec

import pytest

from src.core.category.application.use_cases.exceptions import (
    CategoryAlreadyExistsException,
    CategoryDoesNotExistsException,
    InvalidCategoryData,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            name="Movie",
            description="Some description",
            is_active=True,
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Movie updated",
            description="Some description",
            is_active=True,
        )

        response = use_case.execute(request)

        assert category.name == request.name
        assert category.description == request.description
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_name_with_same_name(self):
        category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Some description",
            is_active=True,
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Movie",
        )

        # with pytest.raises(InvalidCategoryData):
        response = use_case.execute(request)

        # assert category.name == request.name

    def test_update_category_description(self):
        category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Some description",
            is_active=True,
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            description="Some description updated",
        )

        response = use_case.execute(request)

        assert category.name == "Movie"
        assert category.description == "Some description updated"
        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Some description",
            is_active=True,
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=False,
        )

        response = use_case.execute(request)

        assert category.is_active is False
        assert category.name == "Movie"
        assert category.description == "Some description"
        mock_repository.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Some description",
            is_active=False,
        )

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=True,
        )

        response = use_case.execute(request)

        assert category.is_active is True
        assert category.name == "Movie"
        assert category.description == "Some description"
        mock_repository.update.assert_called_once_with(category)

    def test_when_category_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(id=uuid.uuid4())

        with pytest.raises(CategoryDoesNotExistsException) as exc:
            use_case.execute(request)

        mock_repository.update.assert_not_called()
        assert str(exc.value) == f"Category with {request.id} not found"
