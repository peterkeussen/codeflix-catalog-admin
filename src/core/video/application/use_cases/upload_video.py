from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from src.core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus
from src.core.video.domain.video_repository import VideoRepository


class UploadVideo:
    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str

    def __init__(
        self, video_repository: VideoRepository, store_service: AbstractStorageService
    ):
        self.video_repository = video_repository
        self.store_service = store_service

    def execute(self, input: Input) -> None:
        video = self.video_repository.get_by_id(input.video_id)
        if not video:
            raise VideoNotFound(f"Video id {input.video_id} does not exists")

        file_path = Path("videos") / str(video.id) / input.file_name

        self.store_service.store(
            file_path=str(file_path),
            content=input.content,
            content_type=input.content_type,
        )

        audio_video_media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING,
        )

        video.update_video(audio_video_media)

        self.video_repository.update(video)
