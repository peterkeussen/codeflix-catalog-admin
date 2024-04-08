from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repositry import InMemoryGenreRepository


class TestListGenre:
    def test_list_genre_associated_categories(self):
        category_repository = InMemoryCategoryRepository()

        movie = Category(name="Movie")
        category_repository.save(movie)
        documentary = Category(name="Documentary")
        category_repository.save(documentary)

        genre_repository = InMemoryGenreRepository()
        genre = Genre(
            name="Action",
            categories={movie.id, documentary.id},
        )
        genre_repository.save(genre)

        use_case = ListGenre(genre_repository)

        output = use_case.execute(input=ListGenre.Imput())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name="Action",
                    is_active=True,
                    categories={movie.id, documentary.id},
                )
            ]
        )
        assert output.data[0].categories == {movie.id, documentary.id}

    def test_list_genre_is_empty(self):
        genre_repository = InMemoryGenreRepository()

        use_case = ListGenre(genre_repository)

        output = use_case.execute(input=ListGenre.Imput())

        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])
