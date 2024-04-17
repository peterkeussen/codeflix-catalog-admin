from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4


class CastMemberType(StrEnum):
    DIRECTOR = "DIRECTOR"
    ACTOR = "ACTOR"


@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("Name cannot be longer than 255")

        if not self.name:
            raise ValueError("Name cannot be empty")

        if not self.type in CastMemberType.__members__:
            raise ValueError("Type must be a valid CastMemberType: actor or director")

    def __str__(self):
        return f"{self.name} - {self.type}"

    def __repr__(self):
        return f"<CastMember {self.name} {self.type} ({self.id})>"

    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False

        return self.id == other.id

    def update(self, name, type):
        self.name = name
        self.type = type

        self.validate()
