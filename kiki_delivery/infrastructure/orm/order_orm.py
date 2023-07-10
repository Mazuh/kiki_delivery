from typing import Self, List
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, DateTime
from kiki_delivery.domain.order import Order, OrderItem, OrderStatus
from kiki_delivery.infrastructure.orm.customer_orm import CustomerORM
from kiki_delivery.infrastructure.shared.database import Base


class OrderORM(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    status: Mapped[str] = mapped_column(String(25), nullable=False)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=True)
    customer: Mapped["CustomerORM"] = relationship()
    items: Mapped[List["OrderItemORM"]] = relationship()

    def to_entity(self) -> Order:
        return Order(
            id=self.id,
            status=OrderStatus(self.status),
            received_at=self.received_at,
            customer_id=self.customer_id,
            items=[item.to_entity() for item in self.items],
        )

    @classmethod
    def from_entity(cls, order: Order) -> Self:
        return cls(
            id=order.id,
            status=order.status.value,
            received_at=order.received_at,
            customer_id=order.customer_id,
        )


class OrderItemORM(Base):
    __tablename__ = "orders_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    def to_entity(self) -> OrderItem:
        return OrderItem(id=self.id, order_id=self.order_id, product_id=self.product_id)

    @classmethod
    def from_entity(cls, order_item: OrderItem) -> Self:
        return cls(
            id=order_item.id,
            order_id=order_item.order_id,
            product_id=order_item.product_id,
        )
