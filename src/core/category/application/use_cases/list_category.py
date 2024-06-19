from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases.list_output import ListPagOrderSearchUseCase
from src.core.category.domain.category import Category


@dataclass
class ListCategoryRequest:
    order_by: str = "name"
    ordering: str = "asc"
    current_page: int = 1
    page_size: int = 10


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


# @dataclass
# class ListOutputMeta:
#     current_page: int = 1
#     page_size: int = 10
#     total: int = 0


# T = TypeVar("T")


# @dataclass
# class ListOutput(Generic[T], ABC):
#     data: list[T] = field(default_factory=list)
#     meta: ListOutputMeta = field(default_factory=ListOutputMeta)


# @dataclass
# class ListCategoryResponse(ListOutput[CategoryOutput]):
#     pass


class ListCategory(ListPagOrderSearchUseCase[Category, CategoryOutput]):
    @staticmethod
    def get_output_entity(entities: list[Category]) -> list[CategoryOutput]:
        return [
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in entities
        ]

    # def __init__(self, repository: CategoryRepository) -> None:
    #     self.repository = repository

    # def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
    #     categories = self.repository.list()
    #     sorted_categories = sorted(
    #         [
    #             CategoryOutput(
    #                 id=category.id,
    #                 name=category.name,
    #                 description=category.description,
    #                 is_active=category.is_active,
    #             )
    #             for category in categories
    #         ],
    #         key=lambda category: getattr(category, request.order_by),
    #         reverse=False if request.ordering == "asc" else True,
    #     )

    #     page_offset = (request.current_page - 1) * request.page_size
    #     categories_page = sorted_categories[
    #         page_offset : page_offset + request.page_size
    #     ]

    #     return ListCategoryResponse(
    #         data=categories_page,
    #         meta=ListOutputMeta(
    #             current_page=request.current_page,
    #             page_size=request.page_size,
    #             total=len(sorted_categories),
    #         ),
    #     )
