from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_case.exceptions import CastmemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class DeleteCastMemberRequest:
    id: UUID


class DeleteCastMember:
    def __init__(self, repository: CastMemberRepository) -> None:
        self.repository = repository

    def execute(self, request: DeleteCastMemberRequest) -> None:
        cast_member = self.repository.get_by_id(request.id)

        if not cast_member:
            raise CastmemberNotFound(f"CastMember id {request.id} not found")
        self.repository.delete(request.id)
