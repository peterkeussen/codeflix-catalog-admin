from uuid import uuid4

import pytest

from src.core.cast_member.application.use_case.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.use_case.exceptions import CastmemberNotFound
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repositry import (
    InMemoryCastMemberRepository,
)


class TestDeleteCastMember:
    def test_delete_cast_member(self):
        cast_member = CastMember(name="actor", type=CastMemberType.ACTOR)

        repository = InMemoryCastMemberRepository([cast_member])
        use_case = DeleteCastMember(repository)
        input_cast = DeleteCastMember.Input(id=cast_member.id)

        assert repository.get_by_id(cast_member.id) is not None

        use_case.execute(input_cast)

        assert repository.get_by_id(cast_member.id) is None
        assert len(repository.list()) == 0

    def test_delete_cast_member_with_invalid_id(self):
        repository = InMemoryCastMemberRepository()
        use_case = DeleteCastMember(repository)
        input_cast = DeleteCastMember.Input(id=uuid4())

        with pytest.raises(CastmemberNotFound):
            use_case.execute(input_cast)
