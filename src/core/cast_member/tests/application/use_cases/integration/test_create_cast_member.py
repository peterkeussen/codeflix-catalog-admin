import pytest

from src.core.cast_member.application.use_case.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.use_case.exceptions import InvalidCastMemberData
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repositry import (
    InMemoryCastMemberRepository,
)


class TestCreateCastMember:
    def test_create_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Peter", type=CastMemberType.ACTOR)
        use_case = CreateCastMember(repository)

        output = use_case.execute(cast_member)  # type: ignore

        repo_member = repository.get_by_id(output.id)
        assert repo_member.name == cast_member.name  # type: ignore
        assert repo_member.type == cast_member.type  # type: ignore

    def test_create_cast_member_with_invalid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository)
        cast_member = CreateCastMember.Input(name="", type=CastMemberType.ACTOR)

        with pytest.raises(
            InvalidCastMemberData, match="Name cannot be empty"
        ) as error:
            use_case.execute(cast_member)  # type: ignore

        assert error.type == InvalidCastMemberData
        assert str(error.value) == "Name cannot be empty"

    def test_create_cast_member_with_invalid_type(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository)
        cast_member = CreateCastMember.Input(name="Peter", type="")  # type: ignore

        with pytest.raises(
            InvalidCastMemberData,
            match="Type must be a valid CastMemberType: actor or director",
        ):
            use_case.execute(cast_member)
