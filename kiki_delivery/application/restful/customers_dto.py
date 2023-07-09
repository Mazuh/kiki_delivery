from typing import Self, List
from dataclasses import dataclass
from kiki_delivery.application.restful.shared import dto
from kiki_delivery.domain.customer.customer_entities import Customer
from kiki_delivery.domain.customer.customer_value_objects import Email, Cpf


class CustomerPostDTO(dto.RESTfulInputDTO[Customer]):
    first_name: str
    last_name: str
    email: str
    cpf: str

    def to_entity(self):
        return Customer(
            first_name=self.first_name,
            last_name=self.last_name,
            email=Email(self.email),
            cpf=Cpf(self.cpf),
        )


class CustomerPutDTO(CustomerPostDTO):
    id: int
    first_name: str
    last_name: str
    email: str
    cpf: str

    def to_entity(self) -> Customer:
        return Customer(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=Email(self.email),
            cpf=Cpf(self.cpf),
        )


@dataclass
class CustomerDTO(dto.RESTfulItemDTO[Customer]):
    id: int
    first_name: str
    last_name: str
    email: str
    cpf: str

    @classmethod
    def from_entity(cls, customer: Customer) -> Self:
        return cls(
            id=customer.id or -1,
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email.value,
            cpf=customer.cpf.value,
        )


class CustomersDTO(dto.RESTfulCollectionDTO[Customer, CustomerDTO]):
    @classmethod
    def from_entities(cls, customers: List[Customer]):
        return cls(items=[CustomerDTO.from_entity(it) for it in customers])
