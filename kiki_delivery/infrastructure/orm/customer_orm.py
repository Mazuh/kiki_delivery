from typing import Self
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from kiki_delivery.domain.customer import Customer, Email, Cpf
from kiki_delivery.infrastructure.shared.database import Base


class CustomerORM(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False, index=True)

    def to_entity(self) -> Customer:
        return Customer(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=Email(self.email),
            cpf=Cpf(self.cpf),
        )

    @classmethod
    def from_entity(cls, customer: Customer) -> Self:
        return cls(
            first_name=customer.first_name,
            last_name=customer.last_name,
            email=customer.email.value,
            cpf=customer.cpf.value,
        )
