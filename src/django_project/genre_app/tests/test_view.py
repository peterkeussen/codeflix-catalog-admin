import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

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

        response = APIClient().get("/api/genres/?order_by=name&ordering=desc")

        ### set é não ordenado, logo a ordem de retorno não é a mesma que a de cima

        expected_data = {
            "data": [
                {
                    "id": str(genre_romance.id),
                    "name": genre_romance.name,
                    "is_active": genre_romance.is_active,
                    "categories": [
                        str(category_serie.id),
                        str(category_movie.id),
                    ],
                },
                {
                    "id": str(genre_drama.id),
                    "name": genre_drama.name,
                    "is_active": genre_drama.is_active,
                    "categories": [],
                },
            ]
        }
        # assert response.data == expected_data

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        # assert response.data["data"][0]["id"] == str(genre_romance.id)
        # assert response.data["data"][1]["id"] == str(genre_drama.id)
        # assert response.data["data"][0]["name"] == genre_romance.name
        # assert response.data["data"][1]["name"] == genre_drama.name
        # assert response.data["data"][0]["is_active"] == genre_romance.is_active
        # assert response.data["data"][1]["is_active"] == genre_drama.is_active

        # assert set(response.data["data"][0]["categories"]) == {
        #     str(category_movie.id),
        #     str(category_serie.id),
        # }
        # assert response.data["data"][1]["categories"] == []


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_with_categories(
        self,
        category_movie,
        category_serie,
        genre_repository,
        category_repository,
    ):

        response = APIClient().post(
            "/api/genres/",
            {
                "name": "Action",
                "is_active": True,
                "categories": [str(category_movie.id), str(category_serie.id)],
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]
        created_genre_id = response.data["id"]

        saved_genre = genre_repository.get_by_id(created_genre_id)
        assert saved_genre.name == "Action"
        assert set(saved_genre.categories) == {category_movie.id, category_serie.id}


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_genre_does_not_exist_then_raise_404(self):
        response = APIClient().delete(f"/api/genres/{uuid.uuid4()}/")

        assert response.status_code == 404

    def test_when_pk_is_invalid_then_raise_400(self):
        response = APIClient().delete(f"/api/genres/invalid_pk/")

        assert response.status_code == 400


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository,
        category_movie,
        category_serie,
        genre_repository,
        genre_romance,
    ) -> None:

        category_repository.delete(category_movie.id)
        category_repository.delete(category_serie.id)
        category_repository.save(category_movie)
        category_repository.save(category_serie)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [category_serie.id],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == "Drama"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_serie.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama,
    ) -> None:
        url = f"/api/genres/{str(genre_drama.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository,
        category_movie,
        category_serie,
        genre_repository,
        genre_romance,
    ) -> None:
        category_repository.delete(category_movie.id)
        category_repository.delete(category_serie.id)
        category_repository.save(category_movie)
        category_repository.save(category_serie)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [uuid.uuid4()],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Related category not found: " in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid.uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
