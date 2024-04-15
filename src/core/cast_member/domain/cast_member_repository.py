from abc import ABC, abstractmethod
from typing import Union
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember


class CastMemberRepository(ABC):

    @abstractmethod
    def save(self, cast_member: CastMember):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, cast_member_id: UUID) -> Union[CastMember, None]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Union[CastMember, None]:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> Union[list[CastMember], None]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, cast_member_id: UUID):
        raise NotImplementedError

    @abstractmethod
    def update(self, cast_member: CastMember):
        raise NotImplementedError
