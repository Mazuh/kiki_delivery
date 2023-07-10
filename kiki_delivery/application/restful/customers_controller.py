from fastapi import APIRouter, Depends, Response, status
from kiki_delivery.application.restful.customers_dto import (
    CustomerDTO,
    CustomersDTO,
    CustomerPostDTO,
    CustomerPutDTO,
)
from kiki_delivery.domain.customer.customer_driven_ports import AbcCustomerRepository
from kiki_delivery.infrastructure.repositories.customer_repository import (
    CustomerRepository,
)

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_customer(
    customer_dto: CustomerPostDTO,
    customer_repo: AbcCustomerRepository = Depends(CustomerRepository),
):
    customer = customer_dto.to_entity()
    created = customer_repo.create(customer)
    return CustomerDTO.from_entity(created)


@router.get("/")
async def get_customers(
    customer_repo: AbcCustomerRepository = Depends(CustomerRepository),
):
    return CustomersDTO.from_entities(customer_repo.list())


@router.get("/{id}")
async def get_customer(
    id: int,
    response: Response,
    customer_repo: AbcCustomerRepository = Depends(CustomerRepository),
):
    customer = customer_repo.read(id)
    if not customer:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return CustomerDTO.from_entity(customer)


@router.put("/{id}")
async def put_customer(
    id: int,
    response: Response,
    customer_dto: CustomerPutDTO,
    customer_repo: AbcCustomerRepository = Depends(CustomerRepository),
):
    customer = customer_dto.to_entity()

    updated = customer_repo.update(id, customer)
    if not updated:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return CustomerDTO.from_entity(updated)


@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_customer(
    id: int,
    customer_repo: AbcCustomerRepository = Depends(CustomerRepository),
):
    customer_repo.delete(id)
    return dict(id=id)
