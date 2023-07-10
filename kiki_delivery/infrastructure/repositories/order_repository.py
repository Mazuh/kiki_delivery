from typing import Optional, List
from sqlalchemy.orm import joinedload
from kiki_delivery.domain.order import AbcOrderRepository, Order, OrderStatus, OrderItem
from kiki_delivery.infrastructure.shared.db_repository import AbcDatabaseRepository
from kiki_delivery.infrastructure.orm.order_orm import OrderORM, OrderItemORM


class OrderRepository(AbcDatabaseRepository, AbcOrderRepository):
    def create(self, order: Order) -> Order:
        try:
            order_orm = OrderORM.from_entity(order)
            self._session.add(order_orm)

            self._session.commit()
            self._session.refresh(order_orm)
            return order_orm.to_entity()
        except Exception as exc:
            self._session.rollback()
            raise exc

    def read(self, id: int) -> Optional[Order]:
        order_orm = (
            self._session.query(OrderORM)
            .options(joinedload(OrderORM.items))
            .filter(OrderORM.id == id)
            .first()
        )
        return order_orm.to_entity() if order_orm else None

    def list(self) -> List[Order]:
        orders_orm = (
            self._session.query(OrderORM).options(joinedload(OrderORM.items)).all()
        )
        return [c.to_entity() for c in orders_orm]

    def update_status(self, id: int, order: Order) -> Optional[Order]:
        order_orm = self._session.query(OrderORM).filter(OrderORM.id == id).first()
        if order_orm is None:
            return None

        try:
            order_orm.status = order.status.value
            order_orm.received_at = order.received_at

            self._session.commit()
            self._session.refresh(order_orm)

            return order_orm.to_entity()
        except Exception as exc:
            self._session.rollback()
            raise exc

    def delete(self, id: int) -> None:
        order = self._session.query(OrderORM).filter(OrderORM.id == id).first()
        if order is None:
            return

        self._session.delete(order)
        self._session.commit()

    def create_item(self, order_id, item: OrderItem) -> OrderItem:
        assert order_id == item.order_id

        try:
            item_orm = OrderItemORM.from_entity(item)
            self._session.add(item_orm)

            self._session.commit()
            self._session.refresh(item_orm)
            return item_orm.to_entity()
        except Exception as exc:
            self._session.rollback()
            raise exc

    def delete_item(self, id: int, item_id: int) -> None:
        item = (
            self._session.query(OrderItemORM)
            .filter(OrderORM.id == id, OrderItemORM.id == item_id)
            .first()
        )
        if item is None:
            return

        self._session.delete(item)
        self._session.commit()
