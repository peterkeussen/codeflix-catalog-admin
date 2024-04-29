from unittest.mock import create_autospec

from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
    ListOutputMeta,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        category = Category(
            name="Movie",
            description="Some description",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []
        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[], meta=ListOutputMeta(current_page=1, page_size=10, total=0)
        )

    def test_when_categories_in_repository_then_return_a_list(self):
        category_film = Category(
            name="Movie",
            description="Some description",
            is_active=True,
        )
        category_serie = Category(
            name="Serie",
            description="Some description",
            is_active=True,
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category_film, category_serie]
        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_film.id,
                    name=category_film.name,
                    description=category_film.description,
                    is_active=category_film.is_active,
                ),
                CategoryOutput(
                    id=category_serie.id,
                    name=category_serie.name,
                    description=category_serie.description,
                    is_active=category_serie.is_active,
                ),
            ],
            meta=ListOutputMeta(current_page=1, page_size=10, total=2),
        )
