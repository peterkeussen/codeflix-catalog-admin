from dataclasses import dataclass
from uuid import UUID, uuid4

from src.core.cast_member.application.use_case.exceptions import InvalidCastMemberData
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class CreateCastMember:
    def __init__(self, repository: CastMemberRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        name: str
        type: CastMemberType

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        try:
            cast_member = CastMember(
                id=uuid4(),
                name=input.name,
                type=input.type,
            )
        except ValueError as error:
            raise InvalidCastMemberData(error) from error

        self.repository.save(cast_member=cast_member)
        return CreateCastMember.Output(id=cast_member.id)
