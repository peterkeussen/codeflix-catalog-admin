import uuid
from uuid import UUID

import pytest

from src.core.genre.domain.genre import Genre


class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="Name must be less than 255 characters"):
            Genre(name="a" * 256)

    def test_create_genre_with_default_values(self):
        genre = Genre(name="Romance")

        assert genre.name == "Romance"
        assert genre.is_active is True
        assert genre.id
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_create_genre_with_provided_values(self):
        genre_id = uuid.uuid4()
        categories = {uuid.uuid4(), uuid.uuid4()}
        genre = Genre(
            id=genre_id, name="Romance", is_active=False, categories=categories
        )

        assert genre.name == "Romance"
        assert genre.is_active is False

    def test_create_genre_as_active_by_default(self):
        genre = Genre(name="Romance")

        assert genre.is_active is True

    def test_cannot_create_genre_with_invalid_name(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Genre(name="")


class TestChangeName:
    def test_update_genre_with_name(self):
        genre = Genre(name="Romance")

        genre.change_name("Terror")

        assert genre.name == "Terror"

    def test_update_genre_with_invalid_name_raises_exception(self):
        genre = Genre(name="Romance")

        with pytest.raises(ValueError, match="Name must be less than 255 characters"):
            genre.change_name("a" * 256)

    def test_cannot_update_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Genre(name="")


class TestActivate:
    def test_activate_inactive_genre(self):
        genre = Genre(
            name="Romance",
            is_active=False,
        )

        genre.activate()

        assert genre.is_active is True

    def test_activate_active_genre(self):
        genre = Genre(
            name="Romance",
            is_active=True,
        )

        genre.activate()

        assert genre.is_active is True


class TestDeactivate:
    def test_deactivate_active_genre(self):
        genre = Genre(
            name="Romance",
            is_active=True,
        )

        genre.deactivate()

        assert genre.is_active is False

    def test_deactivate_inactive_genre(self):
        genre = Genre(
            name="Romance",
            is_active=False,
        )

        genre.deactivate()

        assert genre.is_active is False


class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        genre_1 = Genre(name="Romance", id=common_id)
        genre_2 = Genre(name="Romance", id=common_id)

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        genre = Genre(name="Romance", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert genre != dummy


class TestAddCategory:
    def test_add_category(self):
        genre = Genre(name="Romance")
        category_id = uuid.uuid4()

        assert category_id not in genre.categories
        genre.add_category(category_id)
        assert category_id in genre.categories


class TestRemoveCategory:
    def test_remove_category(self):
        category_id = uuid.uuid4()
        genre = Genre(name="Romance", categories={category_id})

        assert category_id in genre.categories
        genre.remove_category(category_id)
        assert category_id not in genre.categories
        assert genre.categories == set()

    def test_can_add_multiple_categories(self):
        genre = Genre(name="Romance")
        category_id_1 = uuid.uuid4()
        category_id_2 = uuid.uuid4()

        genre.add_category(category_id_1)
        genre.add_category(category_id_2)

        assert category_id_1 in genre.categories
        assert category_id_2 in genre.categories
