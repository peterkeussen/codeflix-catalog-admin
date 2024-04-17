from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_case.exceptions import CastmemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class DeleteCastMember:
    def __init__(self, repository: CastMemberRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        cast_member = self.repository.get_by_id(input.id)

        if not cast_member:
            raise CastmemberNotFound(f"CastMember id {input.id} not found")
        self.repository.delete(input.id)
