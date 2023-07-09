from typing import Optional, List
from kiki_delivery.domain.customer import AbcCustomerRepository, Customer
from kiki_delivery.infrastructure.shared.db_repository import AbcDatabaseRepository
from kiki_delivery.infrastructure.orm.customer_orm import CustomerORM


class CustomerRepository(AbcDatabaseRepository, AbcCustomerRepository):
    def create(self, customer: Customer) -> Customer:
        customer_orm = CustomerORM.from_entity(customer)
        self._session.add(customer_orm)
        self._session.commit()
        self._session.refresh(customer_orm)
        return customer_orm.to_entity()

    def read(self, id: int) -> Optional[Customer]:
        customer_orm = (
            self._session.query(CustomerORM).filter(CustomerORM.id == id).first()
        )
        return customer_orm.to_entity() if customer_orm else None

    def list(self) -> List[Customer]:
        customers_orm = self._session.query(CustomerORM).all()
        return [c.to_entity() for c in customers_orm]

    def update(self, id: int, customer: Customer) -> Optional[Customer]:
        existing = self._session.query(CustomerORM).filter(CustomerORM.id == id).first()
        if existing is None:
            return None

        updating = CustomerORM.from_entity(customer)

        for key, value in updating.__dict__.items():
            if not key.startswith("_") and key != "id" and value is not None:
                setattr(existing, key, value)

        self._session.commit()
        self._session.refresh(existing)

        return existing.to_entity()

    def delete(self, id: int) -> None:
        customer = self._session.query(CustomerORM).filter(CustomerORM.id == id).first()
        if customer is None:
            return

        self._session.delete(customer)
        self._session.commit()
