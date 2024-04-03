from unittest.mock import create_autospec

from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class TestListGenre:
    def test_genre_list(self):
        movie_category = Category(name="Movie")
        documentary = Category(name="Documentary")

        mock_repository = create_autospec(GenreRepository)
        mock_repository.list.return_value = [
            Genre(
                name="Action",
                categories={movie_category.id, documentary.id},
            )
        ]

        use_case = ListGenre(mock_repository)

        output = use_case.execute(input=ListGenre.Imput())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=mock_repository.list.return_value[0].id,
                    name="Action",
                    is_active=True,
                    categories={movie_category.id, documentary.id},
                )
            ]
        )
