import abc
import random
from typing import TypeVar, Generic, List
from kiki_delivery.domain.shared.repository import (
    AbcFullGenericRepository,
    PotentiallyHasId,
)

T = TypeVar("T", bound=PotentiallyHasId)


class FakeGenericFullRepository(Generic[T], AbcFullGenericRepository[T]):
    _items: List[T]

    def __init__(self):
        self._items = []

    def create(self, entity):
        if not entity.id:
            entity.id = random.randint(1, 100000)

        self._items.append(entity)
        return entity

    def read(self, id):
        for item in self._items:
            if item.id == id:
                return item

        return None

    def list(self):
        return self._items

    def update(self, id, updating):
        self._items = [(updating if item.id == id else item) for item in self._items]
        return updating

    def delete(self, id):
        self._items = [item for item in self._items if item.id != id]
