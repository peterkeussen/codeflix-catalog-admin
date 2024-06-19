from unittest.mock import call, create_autospec

from src.core.category.application.use_cases.list_category import ListCategory
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []
        use_case = ListCategory(repository=mock_repository)
        input = ListCategory.Input()
        output = use_case.execute(input)

        assert len(output.data) == 0

        assert mock_repository.list.call_count == 1

        assert mock_repository.list.call_args_list == [
            call(
                order_by="name",
                ordering="asc",
                current_page=1,
                page_size=10,
                search="",
            )
        ]

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
        input = ListCategory.Input()
        output = use_case.execute(input)

        assert mock_repository.list.call_count == 1

        assert len(output.data) == 2

        assert mock_repository.list.call_args_list == [
            call(
                order_by="name",
                ordering="asc",
                current_page=1,
                page_size=10,
                search="",
            )
        ]

        (movie_category_output, serie_category_output) = output.data

        assert movie_category_output.id == movie_category_output.id
        assert movie_category_output.name == movie_category_output.name
        assert movie_category_output.description == movie_category_output.description
        assert movie_category_output.is_active == movie_category_output.is_active

        assert serie_category_output.id == serie_category_output.id
        assert serie_category_output.name == serie_category_output.name
        assert serie_category_output.description == serie_category_output.description
        assert serie_category_output.is_active == serie_category_output.is_active

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
