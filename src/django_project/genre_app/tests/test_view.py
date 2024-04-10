
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie() -> Category:
    return Category(
        name="Movie",
        description="Movie description",
    )
    

@pytest.fixture
def category_serie() -> Category:
    return Category(
        name="Serie",
        description="Serie description",
    )
    

@pytest.fixture
def category_repository(category_movie, category_serie) -> DjangoORMCategoryRepository:
    repository = DjangoORMCategoryRepository()
    repository.save(category_movie)
    repository.save(category_serie)
    return repository

@pytest.fixture
def genre_romance(category_movie, category_serie) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_movie.id, category_serie.id},
    )
    
@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        is_active=True,
        categories=set(),
    )
    
@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()

@pytest.mark.django_db
class TestListAPI:
    def test_list_genres(
        self,
        genre_romance,
        genre_drama,
        category_movie,
        category_serie,
        genre_repository,
        category_repository,
    ):
        
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)

        response = APIClient().get("/api/genres/")

        ### set é não ordenado, logo a ordem de retorno não é a mesma que a de cima
        
        # expected_data = {
        #     "data": [
        #         {
        #             "id": str(genre_romance.id),
        #             "name": genre_romance.name,
        #             "is_active": genre_romance.is_active,
        #             "categories": [
        #                     str(category_movie.id),
        #                     str(category_serie.id),
        #                 ],
        #         },
        #         {
        #             "id": str(genre_drama.id),
        #             "name": genre_drama.name,
        #             "is_active": genre_drama.is_active,
        #             "categories": [],
        #         },
        #     ]
        # }
        # assert response.data == expected_data

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data["data"][0]["id"] == str(genre_romance.id)
        assert response.data["data"][1]["id"] == str(genre_drama.id)
        assert response.data["data"][0]["name"] == genre_romance.name
        assert response.data["data"][1]["name"] == genre_drama.name
        assert response.data["data"][0]["is_active"] == genre_romance.is_active
        assert response.data["data"][1]["is_active"] == genre_drama.is_active
        
        assert set(response.data["data"][0]["categories"]) == {str(category_movie.id), str(category_serie.id)}
        assert response.data["data"][1]["categories"] == []
        
@pytest.mark.django_db  
class TestCreateAPI:
    def test_create_with_categories(
        self,
        genre_romance,
        genre_drama,
        category_movie,
        category_serie,
        genre_repository,
        category_repository,
    ):
        # genre_repository.save(genre_romance)
        # genre_repository.save(genre_drama)

        response = APIClient().post(
            "/api/genres/",
            {
                "name": "Action",
                "is_active": True,
                "categories": [
                    str(category_movie.id), 
                    str(category_serie.id)
                ],
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        created_genre_id = response.data["id"]
        
        saved_genre = genre_repository.get_by_id(created_genre_id)
        assert saved_genre.name == "Action"
        assert set(saved_genre.categories) == {category_movie.id, category_serie.id}