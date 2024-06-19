from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from src.core._shared import settings
from src.core._shared.domain.entity import Entity
from src.django_project._shared.repository.list_repository import ListRepository

ENTITY = TypeVar("ENTITY", bound=Entity)
ENTITY_OUTPUT = TypeVar("ENTITY_OUTPUT")
ENTITY_OUTPUT_DATA = TypeVar("ENTITY_OUTPUT_DATA")


@dataclass(frozen=True, kw_only=True)
class ListPagOrderSearchUseCase(ABC, Generic[ENTITY, ENTITY_OUTPUT]):

    @dataclass
    class Input:
        order_by: str = "name"
        ordering: str = "asc"
        current_page: int = 1
        page_size: int = 10  # settings.REPOSITORY["page_size"]
        search: str = ""

    @dataclass
    class OutputMeta:
        current_page: int
        page_size: int
        total: int
        num_pages: int

    @dataclass
    class Output(Generic[ENTITY_OUTPUT_DATA], ABC):
        data: list[ENTITY_OUTPUT_DATA]
        meta: "ListPagOrderSearchUseCase.OutputMeta"

    def __init__(self, repository: ListRepository):
        self.repository = repository
        # self.count: int | None = None

    def execute(
        self, input_data: "ListPagOrderSearchUseCase.Input"
    ) -> "ListPagOrderSearchUseCase.Output[ENTITY_OUTPUT]":
        entities = self.repository.list(
            order_by=input_data.order_by,
            ordering=input_data.ordering,
            current_page=input_data.current_page,
            page_size=input_data.page_size,
            search=input_data.search,
        )

        data = self.get_output_entity(entities)

        total = self.repository.count()

        num_pages = (
            1 if total == input_data.page_size else (total // input_data.page_size) + 1
        )
        # total_found = len(data)

        meta = ListPagOrderSearchUseCase.OutputMeta(
            current_page=input_data.current_page,
            page_size=input_data.page_size,
            total=total,
            num_pages=num_pages,
        )

        return ListPagOrderSearchUseCase.Output(data=data, meta=meta)

    @staticmethod
    @abstractmethod
    def get_output_entity(entities: list[ENTITY]) -> list[ENTITY_OUTPUT]:
        pass
