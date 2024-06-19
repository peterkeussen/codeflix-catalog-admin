from typing import Generic, Protocol, TypeVar

ENTITY = TypeVar("ENTITY")


class ListRepository(Protocol, Generic[ENTITY]):
    def list(
        self,
        order_by: str,
        ordering: str,
        current_page: int,
        page_size: int,
        search: str,
    ) -> list[ENTITY]:
        ...
        # raise NotImplementedError

    def count(self) -> int:
        ...
        # raise NotImplementedError
