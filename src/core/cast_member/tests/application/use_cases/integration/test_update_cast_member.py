import pytest

from src.core.cast_member.application.use_case.update_cast_member import (
    UpdateCastMember,
    UpdateCastMemberResquest,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repositry import (
    InMemoryCastMemberRepository,
)


class TestUpdateCastMember:
    def test_update_cast_member(self):
        cast_member = CastMember(
            name="Peter",
            type=CastMemberType.ACTOR,
        )

        repository = InMemoryCastMemberRepository([cast_member])
        use_case = UpdateCastMember(repository)
        input_cast = UpdateCastMemberResquest(
            id=cast_member.id, name="Peter", type=CastMemberType.DIRECTOR
        )
        use_case.execute(input_cast)

        updated_member = repository.get_by_id(cast_member.id)

        assert updated_member
        assert updated_member.name == "Peter"
        assert updated_member.type == CastMemberType.DIRECTOR

    def test_update_cast_member_with_invalid_type(self):
        cast_member = CastMember(
            name="Peter",
            type=CastMemberType.ACTOR,
        )

        repository = InMemoryCastMemberRepository([cast_member])
        use_case = UpdateCastMember(repository)
        input_cast = UpdateCastMemberResquest(
            id=cast_member.id, name="Peter", type=""  # type: ignore
        )

        with pytest.raises(
            ValueError,
            match="Type must be a valid CastMemberType: actor or director",
        ):
            use_case.execute(input_cast)
