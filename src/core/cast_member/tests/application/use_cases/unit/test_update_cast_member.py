from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.cast_member.application.use_case.exceptions import CastmemberNotFound
from src.core.cast_member.application.use_case.update_cast_member import (
    UpdateCastMember,
    UpdateCastMemberResquest,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestUpdateCastMember:
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
    def mock_repository(self) -> CastMemberRepository:
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

    def test_update_cast_member(self, mock_repository, actor):
        mock_repository.get_by_id.return_value = actor
        use_case = UpdateCastMember(mock_repository)
        input = UpdateCastMemberResquest(
            id=actor.id, name="Peter Parker", type=actor.type
        )
        cast_member = use_case.execute(input)

        assert cast_member.id == actor.id
        assert cast_member.name == "Peter Parker"
        assert cast_member.type == actor.type

    def test_update_cast_member_with_empty_repository(
        self, mock_empyt_repository, actor
    ):
        mock_empyt_repository.list.return_value = []
        use_case = UpdateCastMember(mock_empyt_repository)
        input = UpdateCastMemberResquest(
            id=actor.id, name="Peter Parker", type=actor.type
        )
        cast_member = use_case.execute(input)

        assert len(cast_member) == 0

    def test_update_cast_member_with_invalid_id(self, mock_repository):
        mock_repository.get_by_id.return_value = None
        use_case = UpdateCastMember(mock_repository)
        input = UpdateCastMemberResquest(
            id=uuid4(), name="Peter Parker", type=CastMemberType.ACTOR
        )
        with pytest.raises(CastmemberNotFound):
            use_case.execute(input)
