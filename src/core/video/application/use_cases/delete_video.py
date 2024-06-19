from dataclasses import dataclass
from uuid import UUID

from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.video_repository import VideoRepository


class DeleteVideo:
    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        video = self.video_repository.get_by_id(input.id)

        if not video:
            raise VideoNotFound(f"Video id {input.id} does not exists")

        self.video_repository.delete(video)
