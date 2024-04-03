from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import (
    CategoryAlreadyExistsException,
    CategoryDoesNotExistsException,
    InvalidCategoryData,
)


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


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

        # category = self.repository.get_by_id(request.id)
        # if category is None:
        #     raise CategoryDoesNotExistsException(
        #         f"Category with {request.id} not found"
        #     )

        # try:
        #     if request.is_active is True:
        #         category.activate()

        #     if request.is_active is False:
        #         category.deactivate()

        #     current_name = category.name
        #     current_description = category.description

        #     if request.name is not None:
        #         current_name = request.name

        #     if request.description is not None:
        #         current_description = request.description

        #     category.update(name=current_name, description=current_description)
        # except ValueError as error:
        #     raise InvalidCategoryData(error)

        # self.repository.update(category)
