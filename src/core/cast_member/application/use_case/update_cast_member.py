from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_case.exceptions import CastmemberNotFound
from src.core.cast_member.domain.cast_member import CastMemberType


@dataclass
class UpdateCastMemberResquest:
    id: UUID
    name: str
    type: CastMemberType


class UpdateCastMember:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, request: UpdateCastMemberResquest) -> None:
        cast_member = self.repository.get_by_id(request.id)

        if cast_member is None:
            raise CastmemberNotFound(f"CastMember id {request.id} not found")

        cast_member.update(request.name, request.type)
        self.repository.update(cast_member)
        return cast_member
