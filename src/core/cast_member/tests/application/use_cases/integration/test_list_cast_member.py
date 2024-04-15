from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.use_case.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestListCastMember:
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
    def mock_empyt_repository(self):
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = []

        return repository

    @pytest.fixture
    def mock_repository_with_cast_members(self, actor, director):
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = [actor, director]

        return repository

    def test_list_cast_member_with_empty_repository(
        self,
        mock_empyt_repository,
    ):
        use_case = ListCastMember(mock_empyt_repository)

        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 0
        assert output == ListCastMember.Output(data=[])

    def test_list_cast_member_with_repository(
        self,
        mock_repository_with_cast_members,
        actor,
        director,
    ):
        use_case = ListCastMember(mock_repository_with_cast_members)

        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 2
        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(id=actor.id, name=actor.name, type=actor.type),
                CastMemberOutput(
                    id=director.id, name=director.name, type=director.type
                ),
            ]
        )
