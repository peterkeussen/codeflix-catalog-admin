from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_members: list[CastMember] = None) -> None:  # type: ignore
        self.cast_members: list[CastMember] = cast_members or []

    def save(self, cast_member: CastMember) -> None:
        self.cast_members.append(cast_member)

    def get_by_id(self, cast_member_id: UUID) -> CastMember | None:
        for cast_member in self.cast_members:
            if cast_member.id == cast_member_id:
                return cast_member
        return None

    def get_by_name(self, name: str) -> CastMember | None:
        for category in self.cast_members:
            if category.name == name:
                return category
        return None

    def delete(self, cast_member_id: UUID) -> None:
        cast_member = self.get_by_id(cast_member_id=cast_member_id)
        self.cast_members.remove(cast_member)  # type: ignore

    def update(self, cast_member: CastMember) -> None:
        old_cast_member = self.get_by_id(cast_member.id)
        if old_cast_member:
            self.cast_members.remove(old_cast_member)
            self.cast_members.append(cast_member)

    def list(self) -> list[CastMember]:
        return [cast_member for cast_member in self.cast_members]
