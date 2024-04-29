import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def actor() -> CastMember:
    return CastMember(name="Peter", type=CastMemberType.ACTOR)


@pytest.fixture
def director() -> CastMember:
    return CastMember(name="Sara", type=CastMemberType.DIRECTOR)


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_cast_members(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        actor: CastMember,
        director: CastMember,
    ):

        cast_member_repository.save(actor)
        cast_member_repository.save(director)
        response = APIClient().get("/api/cast_members/?order_by=name&ordering=desc")

        expected_data = {
            "data": [
                {
                    "id": str(director.id),
                    "name": director.name,
                    "type": director.type,
                },
                {
                    "id": str(actor.id),
                    "name": actor.name,
                    "type": actor.type,
                },
            ],
            "meta": {"current_page": 1, "page_size": 10, "total": 2},
        }

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2

        assert response.data == expected_data


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        actor: CastMember,
    ):

        response = APIClient().post(
            "/api/cast_members/",
            data={
                "name": actor.name,
                "type": actor.type,
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        cast_member_id = uuid.UUID(response.data["id"])
        cast_member = cast_member_repository.get_by_id(cast_member_id)
        assert cast_member.name == actor.name
        assert cast_member.type == actor.type


@pytest.mark.django_db
class TestUpdateAPI:
    def test_update_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        actor: CastMember,
    ):

        cast_member_repository.save(actor)
        response = APIClient().put(
            f"/api/cast_members/{actor.id}/",
            data={
                "name": "Peter Parker",
                "type": actor.type,
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        cast_member = cast_member_repository.get_by_id(actor.id)
        assert cast_member.name == "Peter Parker"
        assert cast_member.type == actor.type


@pytest.mark.django_db
class TestDeleteAPI:
    def test_delete_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        actor: CastMember,
    ):

        cast_member_repository.save(actor)
        response = APIClient().delete(f"/api/cast_members/{actor.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        cast_member = cast_member_repository.get_by_id(actor.id)
        assert cast_member is None
