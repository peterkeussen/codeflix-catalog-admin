from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repositry import (
    InMemoryCategoryRepository,
)


class TestDeleteCAtegory:
    def test_delete_category_from_repository(self):
        category_film = Category(
            name="Movie",
            description="Some description",
        )
        category_serie = Category(
            name="Serie",
            description="Some description",
        )
        repository = InMemoryCategoryRepository(
            categories=[category_film, category_serie]
        )
        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_film.id)

        assert repository.get_by_id(category_film.id) is not None
        response = use_case.execute(request)
        assert repository.get_by_id(category_film.id) is None
        assert response is None
