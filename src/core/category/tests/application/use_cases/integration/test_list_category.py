from unittest.mock import create_autospec

from src.core._shared.application.use_cases.list_output import ListPagOrderSearchUseCase
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    def test_return_empty_list(self):
        category = Category(
            name="Movie",
            description="Some description",
            is_active=True,
        )
        repository = InMemoryCategoryRepository(categories=[])
        use_case = ListCategory(repository=repository)
        input = ListCategory.Input()
        output = use_case.execute(input)

        assert repository.categories == []

        assert len(output.data) == 0

        assert output.meta == ListPagOrderSearchUseCase.OutputMeta(
            current_page=1, page_size=10, total=0, num_pages=1
        )

        # assert output.data == ListPagOrderSearchUseCase.Output(
        #     [],
        #     ListPagOrderSearchUseCase.OutputMeta(current_page=1, page_size=10, total=0),
        # )

    def test_return_list_of_categories(self):
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
        repository = InMemoryCategoryRepository(
            categories=[category_film, category_serie]
        )
        use_case = ListCategory(repository=repository)
        input = ListCategory.Input()
        output = use_case.execute(input)

        assert len(output.data) == 2

        assert output.meta == ListPagOrderSearchUseCase.OutputMeta(
            current_page=1, page_size=10, total=2, num_pages=1
        )

        assert output.data == [
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
        ]

        # assert response == ListCategoryResponse(
        #     data=[
        #         CategoryOutput(
        #             id=category_film.id,
        #             name=category_film.name,
        #             description=category_film.description,
        #             is_active=category_film.is_active,
        #         ),
        #         CategoryOutput(
        #             id=category_serie.id,
        #             name=category_serie.name,
        #             description=category_serie.description,
        #             is_active=category_serie.is_active,
        #         ),
        #     ],
        #     meta=ListOutputMeta(current_page=1, page_size=10, total=2),
        # )
