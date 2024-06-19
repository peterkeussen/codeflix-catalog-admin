from abc import ABC
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Generic, TypeVar
from uuid import UUID


@dataclass
class ListVideoInput:
    order_by: str = "name"
    ordering: str = "asc"
    current_page: int = 1
    page_size: int = 10


@dataclass
class VideoOutput:
    id: UUID
    title: str
    duration: Decimal


@dataclass
class ListVideoOutputMeta:
    current_page: int
    page_size: int
    total: int


T = TypeVar("T")


@dataclass
class ListVideoOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListVideoOutputMeta = field(default_factory=ListVideoOutputMeta)


@dataclass
class ListVideoResponse(ListVideoOutput[VideoOutput]):
    pass


class ListVideo:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, request: ListVideoInput) -> ListVideoResponse:
        videos = self.repository.list()

        sorted_videos = sorted(
            [
                VideoOutput(id=video.id, title=video.title, duration=video.duration)
                for video in videos
            ],
            key=lambda video: getattr(video, request.order_by),
            reverse=False if request.ordering == "asc" else True,
        )

        page_offset = (request.current_page - 1) * request.page_size
        videos_page = sorted_videos[page_offset : page_offset + request.page_size]

        return ListVideoResponse(
            data=videos_page,
            meta=ListVideoOutputMeta(
                current_page=request.current_page,
                page_size=request.page_size,
                total=len(sorted_videos),
            ),
        )
