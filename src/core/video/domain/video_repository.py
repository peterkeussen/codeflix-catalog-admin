from abc import ABC, abstractmethod
from typing import Union

from src.core.video.domain.video import Video


class VideoRepository(ABC):

    @abstractmethod
    def save(self, video: Video):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, video_id) -> Union[Video, None]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Union[Video, None]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, video: Video) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, video: Video) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Video]:
        raise NotImplementedError
