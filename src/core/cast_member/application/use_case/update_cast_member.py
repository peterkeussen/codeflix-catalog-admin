from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_case.exceptions import CastmemberNotFound
from src.core.cast_member.domain.cast_member import CastMemberType


class UpdateCastMember:
    def __init__(self, repository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str
        type: CastMemberType

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input):
        cast_member = self.repository.get_by_id(input.id)

        if cast_member is None:
            raise CastmemberNotFound(f"CastMember id {input.id} not found")

        cast_member.update(input.name, input.type)
        self.repository.update(cast_member)
        return cast_member
