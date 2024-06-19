from decimal import Decimal
from unittest.mock import create_autospec

from src.core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


class TestUploadVideo:
    def test_upload_video_media_to_media(self):
        video = Video(
            title="test",
            description="test",
            launch_year=2022,
            duration=Decimal(120),
            published=False,
            opened=False,
            rating=Rating.L,
            categories=set(),
            genries=set(),
            cast_members=set(),
        )

        video_repository = InMemoryVideoRepository(videos=[video])
        mock_storage = create_autospec(AbstractStorageService)

        use_case = UploadVideo(
            video_repository=video_repository, store_service=mock_storage
        )

        input = UploadVideo.Input(
            video_id=video.id,
            file_name="test.mp4",
            content=b"test",
            content_type="video/mp4",
        )

        use_case.execute(input)

        assert mock_storage.store.called
        assert mock_storage.store.call_count == 1

        mock_storage.store.assert_called_with(
            file_path=f"videos/{video.id}/test.mp4",
            content=b"test",
            content_type="video/mp4",
        )

        video_repo = video_repository.get_by_id(video.id)
        video_repo.video = AudioVideoMedia(
            name="test.mp4",
            raw_location="videos/{video.id}/test.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
        )
