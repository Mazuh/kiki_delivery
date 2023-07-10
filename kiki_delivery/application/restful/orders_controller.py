from dataclasses import dataclass, field
from typing import Optional, Self, List
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Response, status
from kiki_delivery.application.restful.shared import dto
from kiki_delivery.domain.order import Order, OrderItem, OrderStatus, AbcOrderRepository
from kiki_delivery.infrastructure.repositories.order_repository import (
    OrderRepository,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@dataclass
class OrderItemDTO(dto.RESTfulItemDTO[OrderItem]):
    order_id: int
    product_id: int
    id: Optional[int]

    @classmethod
    def from_entity(cls, order_item: OrderItem) -> Self:
        return cls(
            id=order_item.id,
            order_id=order_item.order_id,
            product_id=order_item.product_id,
        )


@dataclass
class OrderDTO(dto.RESTfulItemDTO[Order]):
    id: int
    status: str
    receveid_at: str
    customer_id: Optional[int]
    items: List[OrderItemDTO]

    @classmethod
    def from_entity(cls, order: Order) -> Self:
        return cls(
            id=order.id or -1,
            status=order.status.value,
            receveid_at=order.received_at.isoformat() if order.received_at else "",
            customer_id=order.customer_id,
            items=[OrderItemDTO.from_entity(item) for item in order.items],
        )


class OrderPostDTO(BaseModel):
    customer_id: Optional[int]

    def to_entity(self):
        return Order(customer_id=self.customer_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_order(
    order_dto: OrderPostDTO,
    order_repo: AbcOrderRepository = Depends(OrderRepository),
):
    order = order_dto.to_entity()
    created = order_repo.create(order)
    return OrderDTO.from_entity(created)


@router.get("/{id}")
async def get_order(
    id: int,
    response: Response,
    order_repo: AbcOrderRepository = Depends(OrderRepository),
):
    order = order_repo.read(id)
    if not order:
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    return OrderDTO.from_entity(order)


class OrdersDTO(dto.RESTfulCollectionDTO[Order, OrderDTO]):
    @classmethod
    def from_entities(cls, products: List[Order]):
        return cls(items=[OrderDTO.from_entity(it) for it in products])


@router.get("/")
async def get_orders(
    order_repo: AbcOrderRepository = Depends(OrderRepository),
):
    return OrdersDTO.from_entities(order_repo.list())


class OrderItemPostDTO(BaseModel):
    order_id: int
    product_id: int

    def to_entity(self):
        return OrderItem(order_id=self.order_id, product_id=self.product_id)

    @classmethod
    def from_entity(cls, order_item: OrderItem) -> Self:
        return cls(order_id=order_item.order_id, product_id=order_item.product_id)


@router.post("/{order_id}/items", status_code=status.HTTP_201_CREATED)
async def post_order_item(
    order_id: int,
    response: Response,
    item_dto: OrderItemPostDTO,
    order_repo: AbcOrderRepository = Depends(OrderRepository),
):
    if not order_repo.read(order_id):
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    item = item_dto.to_entity()
    created_item = order_repo.create_item(order_id, item)
    return OrderItemDTO.from_entity(created_item)


class OrderStatusPutDTO(BaseModel):
    status: str


@router.put("/{id}/status")
async def put_order_status(
    id: int,
    response: Response,
    status_dto: OrderStatusPutDTO,
    order_repo: AbcOrderRepository = Depends(OrderRepository),
):
    order = order_repo.read(id)
    if not order:
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    order.status = OrderStatus(status_dto.status)

    updated = order_repo.update_status(id, order)
    if not updated:
        response.status_code = status.HTTP_403_FORBIDDEN
        return

    return OrderDTO.from_entity(updated)


@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_order(
    id: int,
    order_repo: AbcOrderRepository = Depends(OrderRepository),
):
    order_repo.delete(id)
    return dict(id=id)
