import abc
from typing import TypeVar, Generic, Self, Optional, List
from dataclasses import dataclass, field
from pydantic import BaseModel

TEntity = TypeVar("TEntity")


class RESTfulInputDTO(Generic[TEntity], abc.ABC, BaseModel):
    @abc.abstractmethod
    def to_entity(self) -> TEntity:
        ...


class RESTfulItemDTO(Generic[TEntity], abc.ABC):
    @abc.abstractclassmethod
    def from_entity(cls, entity: TEntity) -> Self:
        ...


TItem = TypeVar("TItem", bound=RESTfulItemDTO)


@dataclass
class RESTfulCollectionDTO(Generic[TEntity, TItem], abc.ABC):
    items: List[TItem] = field(default_factory=list)

    @abc.abstractclassmethod
    def from_entities(cls, collection: List[TItem]) -> Self:
        ...
