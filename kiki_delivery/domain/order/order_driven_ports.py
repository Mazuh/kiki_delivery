import abc
from typing import Optional, List
from kiki_delivery.domain.order import Order, OrderStatus, OrderItem


class AbcOrderRepository(abc.ABC):
    def create(self, order: Order) -> Order:
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, id: int) -> Optional[Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def update_status(self, id: int, status: Order) -> Optional[Order]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError

    def create_item(self, order_id: int, OrderItem: OrderItem) -> OrderItem:
        raise NotImplementedError

    def delete_item(self, order_id: int, item_id: int) -> None:
        raise NotImplementedError
