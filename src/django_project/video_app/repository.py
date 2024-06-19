from os import name
from uuid import UUID

from django.db import transaction

from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.django_project.video_app.models import AudioVideoMedia as AudioVideoMediaORM
from src.django_project.video_app.models import Video as VideoORM


class DjangoORMVideoRepository(VideoRepository):
    def save(self, video: Video):
        with transaction.atomic():
            video_orm = VideoORM.objects.create(
                id=video.id,
                title=video.title,
                description=video.description,
                launch_year=video.launch_year,
                opened=video.opened,
                rating=video.rating,
                duration=video.duration,
            )
            video_orm.categories.set(video.categories)
            video_orm.genres.set(video.genries)
            video_orm.cast_members.set(video.cast_members)

    def get_by_id(self, video_id: UUID) -> Video | None:
        try:
            video_orm = VideoORM.objects.get(id=video_id)

            return Video(
                id=video_orm.id,
                title=video_orm.title,
                description=video_orm.description,
                launch_year=video_orm.launch_year,
                duration=video_orm.duration,
                opened=video_orm.opened,
                rating=Rating(video_orm.rating),
                published=video_orm.published,
                categories=set(video_orm.categories.values_list("id", flat=True)),
                genries=set(video_orm.genres.values_list("id", flat=True)),
                cast_members=set(video_orm.cast_members.values_list("id", flat=True)),
            )

        except VideoORM.DoesNotExist:
            return None

    def get_by_name(self, name: str) -> Video | None:
        try:
            video_orm = VideoORM.objects.get(title=name)
            return Video(
                id=video_orm.id,
                title=video_orm.title,
                description=video_orm.description,
                launch_year=video_orm.launch_year,
                duration=video_orm.duration,
                opened=video_orm.opened,
                rating=Rating(video_orm.rating),
                published=video_orm.published,
                categories=set(video_orm.categories.values_list("id", flat=True)),
                genries=set(video_orm.genres.values_list("id", flat=True)),
                cast_members=set(video_orm.cast_members.values_list("id", flat=True)),
            )

        except VideoORM.DoesNotExist:
            return None

    # def get_by_title(self, title: str):
    #     pass

    def delete(self, video: Video):
        VideoORM.objects.filter(id=video.id).delete()

    def update(self, video: Video):
        try:
            video_orm = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None
        else:
            with transaction.atomic():
                AudioVideoMediaORM.objects.filter(id=video.id).delete()

                video_orm.categories.set(video.categories)
                video_orm.genres.set(video.genries)
                video_orm.cast_members.set(video.cast_members)

                video_orm.video = (
                    AudioVideoMediaORM.objects.create(
                        name=video.video.name,
                        raw_location=video.video.raw_location,
                        encoded_location=video.video.encoded_location,
                        status=video.video.status,
                    )
                    if video.video
                    else None
                )

                video_orm.title = video.title
                video_orm.description = video.description
                video_orm.opened = video.opened
                video_orm.rating = video.rating
                video_orm.duration = video.duration
                video_orm.launch_year = video.launch_year

                video_orm.save()

    def list(self):
        # TODO: Implementar o list usando ModelMapper
        raise NotImplementedError
