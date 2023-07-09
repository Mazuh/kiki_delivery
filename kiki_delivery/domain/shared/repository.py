import abc
import random
from typing import Protocol, TypeVar, Generic, Optional, List


class PotentiallyHasId(Protocol):
    id: Optional[int]


T = TypeVar("T", bound=PotentiallyHasId)


class AbcFullGenericRepository(Generic[T], abc.ABC):
    @abc.abstractmethod
    def create(self, entity: T) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, id: int) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, id: int, updating: T) -> Optional[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError
