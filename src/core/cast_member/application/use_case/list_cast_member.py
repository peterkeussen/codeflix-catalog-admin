from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


class ListCastMember:
    def __init__(self, repository):
        self.repository = repository

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[CastMemberOutput]

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list()

        mapper_cast_members = [
            CastMemberOutput(
                id=cast_member.id, name=cast_member.name, type=cast_member.type
            )
            for cast_member in cast_members
        ]

        return ListCastMember.Output(data=mapper_cast_members)
