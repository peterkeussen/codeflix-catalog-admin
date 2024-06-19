from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.category.application.exceptions import (
    CategoryDoesNotExistsException,
    InvalidCategoryData,
)


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class UpdateCategory:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)
        if category is None:
            raise CategoryDoesNotExistsException(
                f"Category with {request.id} not found"
            )

        try:
            name = category.name
            description = category.description

            if request.name is not None:
                # founded = self.repository.get_by_name(request.name)
                # if founded:
                #     raise CategoryAlreadyExistsException(
                #         f"Category {request.name} already exists"
                #     )
                name = request.name

            if request.description is not None:
                description = request.description

            if request.is_active is True:
                category.activate()

            if request.is_active is False:
                category.deactivate()

            category.update(name=name, description=description)
        except ValueError as error:
            raise InvalidCategoryData(error)

        self.repository.update(category)
