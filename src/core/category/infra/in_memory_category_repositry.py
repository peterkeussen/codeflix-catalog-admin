from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories=None):
        self.categories = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)

    def get_by_id(self, category_id: UUID) -> Category | None:
        for category in self.categories:
            if category.id == category_id:
                return category
        return None

    def get_by_name(self, name: str) -> Category | None:
        for category in self.categories:
            if category.name == name:
                return category
        return None

    def delete(self, id: UUID) -> None:
        category = self.get_by_id(id)
        self.categories.remove(category)

    def update(self, category: Category) -> None:
        old_category = self.get_by_id(category.id)
        if old_category:
            self.categories.remove(old_category)
            self.categories.append(category)

    def list(
        self,
        order_by: str = "name",
        ordering: str = "asc",
        current_page: int = 1,
        page_size: int = 10,
        search: str = "",
    ) -> list[Category]:
        return [category for category in self.categories]

    def count(self) -> int:
        return len(self.categories)
