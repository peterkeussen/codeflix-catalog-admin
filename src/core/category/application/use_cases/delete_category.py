from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import (
    CategoryDoesNotExistsException,
)
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: DeleteCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)
        if not category:
            raise CategoryDoesNotExistsException(
                f"Category id {request.id} does not exists"
            )
        self.repository.delete(category.id)  # type: ignore
