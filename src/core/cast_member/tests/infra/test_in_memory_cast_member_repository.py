import pytest

from src.core.cast_member.application.use_case.create_cast_member import (
    CreateCastMember,
    CreateCastMemberRequest,
)
from src.core.cast_member.application.use_case.exceptions import InvalidCastMemberData
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repositry import (
    InMemoryCastMemberRepository,
)


class TestSaveCastMember:
    def test_save_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Peter Parker", type="ACTOR")
        repository.save(cast_member)

        assert len(repository.cast_members) == 1
        assert repository.cast_members[0].name == "Peter Parker"
        assert repository.cast_members[0].type == "ACTOR"


class TestGetByIdCastMember:
    def test_get_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Peter Parker", type="ACTOR")
        repository.save(cast_member)

        cast_member = repository.get_by_id(cast_member.id)

        assert cast_member
        assert cast_member.id == cast_member.id
        assert cast_member.name == "Peter Parker"
        assert cast_member.type == "ACTOR"


class TestGetByNameCastMember:
    def test_get_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Peter Parker", type="ACTOR")
        repository.save(cast_member)

        cast_member = repository.get_by_name(cast_member.name)

        assert cast_member
        assert cast_member.id == cast_member.id
        assert cast_member.name == "Peter Parker"
        assert cast_member.type == "ACTOR"


class TestListCastMember:
    def test_list_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Peter Parker", type="ACTOR")
        repository.save(cast_member)

        cast_members = repository.list()

        assert len(cast_members) == 1
        assert cast_members[0].id == cast_member.id
        assert cast_members[0].name == "Peter Parker"
        assert cast_members[0].type == "ACTOR"


class TestUpdateCastMember:
    def test_update_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Peter Parker", type="ACTOR")
        repository.save(cast_member)

        cast_member.name = "Spiderman"
        cast_member.type = "ACTOR"
        repository.update(cast_member)

        cast_member = repository.get_by_id(cast_member.id)

        assert cast_member
        assert cast_member.id == cast_member.id
        assert cast_member.name == "Spiderman"
        assert cast_member.type == "ACTOR"


class TestDeleteCastMember:
    def test_delete_cast_member(self):
        repository = InMemoryCastMemberRepository()
        cast_member = CastMember(name="Peter Parker", type="ACTOR")
        repository.save(cast_member)

        repository.delete(cast_member.id)

        cast_member = repository.get_by_id(cast_member.id)

        assert cast_member is None
