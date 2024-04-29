from uuid import UUID

from django.db import transaction

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, model: CastMemberORM | None = None) -> None:
        self.model = model or CastMemberORM

    def save(self, cast_member: CastMember):
        with transaction.atomic():
            cast_member_orm = CastMemberORM.objects.create(
                id=cast_member.id, name=cast_member.name, type=cast_member.type
            )
            cast_member_orm.save()

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member = self.model.objects.get(id=id)
            return CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            )
        except self.model.DoesNotExist:
            return None

    def get_by_name(self, name: str) -> CastMember | None:
        try:
            cast_member = self.model.objects.get(name=name)
            return CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=CastMemberType(cast_member.type),
            )
        except self.model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.model.objects.filter(id=id).delete()

    def list(self) -> list[CastMember]:
        cast_members = self.model.objects.all()
        return [
            CastMember(
                id=cast_member.id,
                name=cast_member.name,
                type=CastMemberType(cast_member.type),
            )
            for cast_member in cast_members
        ]

    def update(self, cast_member: CastMember) -> None:
        self.model.objects.filter(id=cast_member.id).update(
            name=cast_member.name, type=cast_member.type
        )
