from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)


class TestUpdateCategory:
    def test_update_category_name_and_description(self):
        category = Category(
            name="Movie",
            description="Some description",
            is_active=True,
        )
        repository = InMemoryCategoryRepository([category])

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Movie updated",
            description="Some description updated",
            is_active=False,
        )

        response = use_case.execute(request)

        updated_category = repository.get_by_id(category.id)
        assert updated_category.id == category.id
        assert updated_category.name == "Movie updated"
        assert updated_category.description == "Some description updated"
        assert updated_category.is_active is False
