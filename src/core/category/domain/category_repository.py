from abc import ABC, abstractmethod
from typing import Union

from src.core.category.domain.category import Category


class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category: Category):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, category_id) -> Union[Category, None]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Union[Category, None]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        order_by: str = "name",
        ordering: str = "asc",
        current_page: int = 1,
        page_size: int = 10,
        search: str = "",
    ) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError
