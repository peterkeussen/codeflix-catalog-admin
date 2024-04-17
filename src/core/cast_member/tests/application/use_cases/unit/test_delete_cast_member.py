from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.cast_member.application.use_case.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.use_case.exceptions import CastmemberNotFound
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestDeleteCastMember:
    @pytest.fixture
    def mock_repository(self) -> CastMemberRepository:
        return create_autospec(CastMemberRepository)

    @pytest.fixture
    def actor(self):
        return CastMember(name="actor", type=CastMemberType.ACTOR)

    @pytest.fixture
    def director(self):
        return CastMember(name="director", type=CastMemberType.DIRECTOR)

    @pytest.fixture
    def mock_repository_with_cast_members(self, actor, director):
        repository = create_autospec(CastMemberRepository)
        repository.list.return_value = [actor, director]

        return repository

    def test_delete_cast_member(self, mock_repository, actor):
        mock_repository.get_by_id.return_value = actor
        use_case = DeleteCastMember(mock_repository)
        input_cast = DeleteCastMember.Input(id=actor.id)
        use_case.execute(input_cast)

        mock_repository.delete.assert_called_once_with(actor.id)

    def test_delete_cast_member_with_invalid_id(self, mock_repository):
        mock_repository.get_by_id.return_value = None
        use_case = DeleteCastMember(mock_repository)

        with pytest.raises(CastmemberNotFound):
            use_case.execute(DeleteCastMember.Input(id=uuid4()))
