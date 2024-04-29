from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.use_case.create_cast_member import (
    CreateCastMember,
    CreateCastMemberRequest,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@pytest.fixture
def actor(self):
    return CastMember(
        name="Peter",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def director(self):
    return CastMember(
        name="Christopher",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def mock_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)


@pytest.fixture
def mock_empyt_repository(self):
    repository = create_autospec(CastMemberRepository)
    repository.list.return_value = []

    return repository


@pytest.fixture
def mock_repository_with_cast_members(self, actor, director):
    repository = create_autospec(CastMemberRepository)
    repository.list.return_value = [actor, director]

    return repository


class TestCreateCastMember:
    def test_create_cast_member(self, mock_repository):
        use_case = CreateCastMember(mock_repository)
        input_param = CreateCastMemberRequest(
            name="Peter",
            type=CastMemberType.ACTOR,
        )

        use_case.execute(input_param)

    def test_create_cast_member_with_invalid_name(self, mock_repository):
        use_case = CreateCastMember(mock_repository)

        with pytest.raises(Exception) as exc:
            use_case.execute(
                CreateCastMemberRequest(
                    name="",
                    type=CastMemberType.ACTOR,
                )
            )

        assert str(exc.value) == "Name cannot be empty"

    def test_create_cast_member_with_invalid_type(self, mock_repository):
        use_case = CreateCastMember(mock_repository)

        with pytest.raises(Exception) as exc:
            use_case.execute(
                CreateCastMemberRequest(
                    name="Peter",
                    type="",
                )
            )

        assert (
            str(exc.value) == "Type must be a valid CastMemberType: actor or director"
        )

    # def test_create_cast_member_with_invalid_name_and_type(self, mock_repository):
    #     use_case = CreateCastMember(mock_repository)

    #     with pytest.raises(Exception) as exc:
    #         use_case.execute(
    #             CreateCastMember.Input(
    #                 name="",
    #                 type="",
    #             )
    #         )

    #     assert (
    #         str(exc.value) == "Type must be a valid CastMemberType: actor or director"
    #     )
