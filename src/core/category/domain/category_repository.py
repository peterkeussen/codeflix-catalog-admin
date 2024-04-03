from abc import ABC, abstractmethod
from uuid import UUID

from src.core.category.domain.category import Category


class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category: Category):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, category_id) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Category | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Category]:
        raise NotImplementedError
