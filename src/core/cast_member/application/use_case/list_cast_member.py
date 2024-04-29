from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType


@dataclass
class ListCastMemberRequest:
    order_by: str = "name"
    ordering: str = "asc"
    current_page: int = 1
    page_size: int = 10


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


@dataclass
class ListCastMemberOutputMeta:
    current_page: int
    page_size: int
    total: int


T = TypeVar("T")


@dataclass
class ListCastMemberOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListCastMemberOutputMeta = field(default_factory=ListCastMemberOutputMeta)


@dataclass
class ListCastMemberResponse(ListCastMemberOutput[CastMemberOutput]):
    pass


class ListCastMember:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, request: ListCastMemberRequest) -> ListCastMemberResponse:
        cast_members = self.repository.list()

        sorted_cast_members = sorted(
            [
                CastMemberOutput(
                    id=cast_member.id, name=cast_member.name, type=cast_member.type
                )
                for cast_member in cast_members
            ],
            key=lambda cast_member: getattr(cast_member, request.order_by),
            reverse=False if request.ordering == "asc" else True,
        )

        page_offset = (request.current_page - 1) * request.page_size
        cast_members_page = sorted_cast_members[
            page_offset : page_offset + request.page_size
        ]

        return ListCastMemberResponse(
            data=cast_members_page,
            meta=ListCastMemberOutputMeta(
                current_page=request.current_page,
                page_size=request.page_size,
                total=len(sorted_cast_members),
            ),
        )
