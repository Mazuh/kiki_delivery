from dataclasses import dataclass, field
from typing import Optional, Self, List
from datetime import datetime
from kiki_delivery.domain.order.order_value_objects import OrderStatus
from kiki_delivery.domain.shared.exceptions import DomainLogicalException


@dataclass
class OrderItem:
    order_id: int
    product_id: int
    id: Optional[int] = None


class Order:
    def __init__(
        self,
        id: Optional[int] = None,
        status: Optional[OrderStatus] = OrderStatus("UNCONFIRMED"),
        items: Optional[List[OrderItem]] = None,
        received_at: Optional[datetime] = None,
        customer_id: Optional[int] = None,
    ):
        self.id = id

        if status is None:
            self._status = OrderStatus("UNCONFIRMED")
        else:
            self._status = status

        if items is None:
            self.items = list()
        else:
            self.items = items

        self.received_at = received_at
        self.customer_id = customer_id

    @property
    def status(self) -> OrderStatus:
        return self._status

    @status.setter
    def status(self, new_status: OrderStatus):
        if self.status == new_status:
            return

        ordered_steps = [
            OrderStatus("UNCONFIRMED"),
            OrderStatus("RECEIVED"),
            OrderStatus("IN_PROGRESS"),
            OrderStatus("READY"),
            OrderStatus("FINISHED"),
        ]

        current_index = (
            ordered_steps.index(self.status) if self.status in ordered_steps else -1
        )
        new_index = (
            ordered_steps.index(new_status) if new_status in ordered_steps else -1
        )
        if new_index < 0:
            raise DomainLogicalException("Status change had unexpected new value.")

        if (current_index + 1) != new_index:
            raise DomainLogicalException("Status change not allowed.")

        if new_status == OrderStatus("RECEIVED") and not self.items:
            raise DomainLogicalException("Can't checkout an order without items.")

        self._status = new_status

        if self.status == OrderStatus("RECEIVED"):
            self.received_at = datetime.now()
