from uuid import uuid4

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(
            TypeError,
            match="missing 2 required positional arguments: 'name' and 'type'",
        ):
            CastMember()

    def test_name_cannot_be_longer_than_255_characters(self):
        with pytest.raises(ValueError, match="Name cannot be longer than 255"):
            CastMember(name="a" * 257, type=CastMemberType.ACTOR)

    def test_name_cannot_be_empty(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            CastMember(name="", type=CastMemberType.ACTOR)

    def test_type_cannot_be_empty(self):
        with pytest.raises(
            ValueError,
            match="Type must be a valid CastMemberType: actor or director",
        ):
            CastMember(name="Peter", type="")

    def test_type_cannot_be_invalid(self):
        with pytest.raises(
            ValueError,
            match="Type must be a valid CastMemberType: actor or director",
        ):
            CastMember(name="Peter", type="invalid")

    def test_cast_member_is_not_equal(self):
        actor = CastMember(name="Peter", type=CastMemberType.ACTOR)
        director = CastMember(name="Christopher", type=CastMemberType.DIRECTOR)

        assert actor.__eq__(director) is False

    def test_cast_member_is_equal(self):
        actor = CastMember(name="Peter", type=CastMemberType.ACTOR)
        new_actor = actor

        assert actor.__eq__(new_actor)

    def test_cast_member_str(self):
        actor = CastMember(name="Peter", type=CastMemberType.ACTOR)

        assert str(actor) == "Peter - ACTOR"

    def test_create_cast_member_with_valid_data(self):
        actor_id = uuid4()
        actor = CastMember(id=actor_id, name="Peter", type=CastMemberType.ACTOR)

        assert actor.id == actor_id
        assert actor.name == "Peter"
        assert actor.type == CastMemberType.ACTOR
