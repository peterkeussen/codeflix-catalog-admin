import uuid
from uuid import UUID

import pytest

from src.core.category.domain.category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="Name must be less than 255 characters"):
            Category(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name="Movie")

        assert category.id
        assert isinstance(category.id, UUID)

    def test_create_category_with_default_values(self):
        category = Category(name="Movie")

        assert category.name == "Movie"
        assert category.description == ""
        assert category.is_active is True

    def test_create_category_with_provided_values(self):
        category = Category(
            name="Movie", description="Some description", is_active=False
        )

        assert category.name == "Movie"
        assert category.description == "Some description"
        assert category.is_active is False

    def test_create_category_as_active_by_default(self):
        category = Category(name="Movie")

        assert category.is_active is True

    def test_cannot_create_category_with_invalid_name(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Category(name="")


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Movie", description="Some description")

        category.update("Movie 2", "Some description 2")

        assert category.name == "Movie 2"
        assert category.description == "Some description 2"

    def test_update_category_with_invalid_name_raises_exception(self):
        category = Category(name="Movie", description="Some description")

        with pytest.raises(ValueError, match="Name must be less than 255 characters"):
            category.update("a" * 256, "Some description 2")

    def test_cannot_update_category_with_empty_name(self):
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Category(name="")


class TestActivate:
    def test_activate_inactive_category(self):
        category = Category(
            name="Movie",
            description="Some description",
            is_active=False,
        )

        category.activate()

        assert category.is_active is True

    def test_activate_active_category(self):
        category = Category(
            name="Movie",
            description="Some description",
            is_active=True,
        )

        category.activate()

        assert category.is_active is True


class TestDeactivate:
    def test_deactivate_active_category(self):
        category = Category(
            name="Movie",
            description="Some description",
            is_active=True,
        )

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_inactive_category(self):
        category = Category(
            name="Movie",
            description="Some description",
            is_active=False,
        )

        category.deactivate()

        assert category.is_active is False


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category(name="Filme", id=common_id)
        category_2 = Category(name="Filme", id=common_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = Category(name="Filme", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy
