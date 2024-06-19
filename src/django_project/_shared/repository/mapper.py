from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from django.db.models import Model

ENTITY = TypeVar("ENTITY")
MODEL = TypeVar("MODEL", bound=Model)


class EntityModelMapper(ABC, Generic[ENTITY, MODEL]):
    @staticmethod
    @abstractmethod
    def to_model(entity: ENTITY, save: bool = False) -> MODEL:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def to_entity(model: MODEL) -> ENTITY:
        raise NotImplementedError
