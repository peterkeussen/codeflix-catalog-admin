import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.models import CastMember as CastMemberORM
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.mark.django_db
class TestSave:
    def test_saves_cast_member_in_database(self):
        cast_member = CastMember(
            name="Peter",
            type=CastMemberType.ACTOR,
        )
        repository = DjangoORMCastMemberRepository()

        assert CastMemberORM.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberORM.objects.count() == 1

        repository_saved_cast_member = CastMemberORM.objects.first()
        assert repository_saved_cast_member.id == cast_member.id
        assert repository_saved_cast_member.name == cast_member.name
        assert repository_saved_cast_member.type == cast_member.type

        assert CastMemberORM.objects.first().name == "Peter"
        assert CastMemberORM.objects.first().type == CastMemberType.ACTOR


@pytest.mark.django_db
class TestUpdate:
    def test_updates_cast_member_in_database(self):
        cast_member = CastMember(
            name="Peter",
            type=CastMemberType.ACTOR,
        )
        repository = DjangoORMCastMemberRepository()
        assert CastMemberORM.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberORM.objects.count() == 1
        cast_member.update("Peter updated", CastMemberType.DIRECTOR)
        repository.update(cast_member)
        assert CastMemberORM.objects.count() == 1
        repository_saved_cast_member = CastMemberORM.objects.first()
        assert repository_saved_cast_member.name == "Peter updated"
        assert repository_saved_cast_member.type == cast_member.type


@pytest.mark.django_db
class TestList:
    def test_returns_list_of_cast_members(self):
        cast_member = CastMember(
            name="Peter",
            type=CastMemberType.ACTOR,
        )
        repository = DjangoORMCastMemberRepository()
        assert CastMemberORM.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberORM.objects.count() == 1
        cast_members = repository.list()
        assert repository.list() == [cast_member]
        assert len(cast_members) == 1
        assert cast_members[0].name == cast_member.name
        assert cast_members[0].type == cast_member.type

        assert CastMemberORM.objects.first().name == "Peter"
        assert CastMemberORM.objects.first().type == CastMemberType.ACTOR


@pytest.mark.django_db
class TestGetByName:
    def test_returns_cast_member_by_name(self):
        cast_member = CastMember(
            name="Peter",
            type=CastMemberType.ACTOR,
        )
        repository = DjangoORMCastMemberRepository()
        assert CastMemberORM.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberORM.objects.count() == 1
        cast_member = repository.get_by_name("Peter")
        assert cast_member.name == "Peter"
        assert cast_member.type == CastMemberType.ACTOR


@pytest.mark.django_db
class TestDelete:
    def test_deletes_cast_member_from_database(self):
        cast_member = CastMember(
            name="Peter",
            type=CastMemberType.ACTOR,
        )
        repository = DjangoORMCastMemberRepository()
        assert CastMemberORM.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberORM.objects.count() == 1
