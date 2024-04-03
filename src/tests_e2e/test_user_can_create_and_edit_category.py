import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_create_and_edit_category(self):
        api_client = APIClient()

        # Verifica que a lista está vazia
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": []}

        # Cria uma categoria
        create_response = api_client.post(
            "/api/categories/",
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]

        # Verifica que a categoria foi criada
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ]
        }

        # Edita da informação da categoria
        update_response = api_client.put(
            f"/api/categories/{created_category_id}/",
            data={
                "name": "Movie 2",
                "description": "Movie description 2",
                "is_active": True,
            },
        )
        assert update_response.status_code == 204

        # Verifica que a categoria foi editada
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie 2",
                    "description": "Movie description 2",
                    "is_active": True,
                },
            ]
        }

        # Editar parcialmente a categoria
        partial_update_response = api_client.patch(
            f"/api/categories/{created_category_id}/",
            data={
                "name": "Movie 3",
            },
        )
        assert partial_update_response.status_code == 204

        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie 3",
                    "description": "Movie description 2",
                    "is_active": True,
                },
            ]
        }

        # Deleta a categoria
        delete_response = api_client.delete(f"/api/categories/{created_category_id}/")
        assert delete_response.status_code == 204
