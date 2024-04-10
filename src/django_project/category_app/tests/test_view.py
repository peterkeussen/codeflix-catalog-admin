import uuid

import pytest
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


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
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_categories(
        self,
        category_movie: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):

        category_repository.save(category_movie)
        category_repository.save(category_serie)

        response = APIClient().get("/api/categories/")

        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
                },
                {
                    "id": str(category_serie.id),
                    "name": category_serie.name,
                    "description": category_serie.description,
                    "is_active": category_movie.is_active,
                },
            ]
        }
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_uuid_is_valid(self):
        url = "/api/categories/2168544213243/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_serie)

        response = APIClient().get(f"/api/categories/{category_movie.id}/")

        expected_data = {
            "data": {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_not_exist(self):
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        # assert response.data == expected_data


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_playload_is_valid_then_return_400(self):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Movie description",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
        }

    def test_when_playload_is_valid_then_create_category_and_then_return_201(
        self,
        category_repository: DjangoORMCategoryRepository,
    ):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_category_id = uuid.UUID(response.data["id"])
        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name="Movie",
            description="Movie description",
            is_active=True,
        )

        assert category_repository.list() == [
            Category(
                id=created_category_id,
                name="Movie",
                description="Movie description",
                is_active=True,
            )
        ]

    def test_return_404_when_not_exist(self):
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        # assert response.data == expected_data


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = "/api/categories/2168544213243/"
        response = APIClient().put(
            url,
            data={
                "name": "",
                "description": "Movie description",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."],
        }

    def test_when_payload_is_valid_then_update_category_and_then_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().put(
            url,
            data={
                "name": "Serie",
                "description": "Serie description",
                "is_active": False,
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category.name == "Serie"
        assert updated_category.description == "Serie description"

    def test_partial_update_category_and_return_204(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "name": "Serie 2",
                "description": "Serie description",
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category.name == "Serie 2"
        assert updated_category.description == "Serie description"

    def test_when_category_not_exist_then_return_404(self):
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": "Serie",
                "description": "Serie description",
                "is_active": False,
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_id_uuid_is_valid(self):
        url = "/api/categories/2168544213243/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_category_not_exist_then_return_404(self):
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_exist_then_return_204(
        self, category_movie: Category, category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.get_by_id(category_movie.id) is None
        assert category_repository.list() == []
