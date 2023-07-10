from kiki_delivery.domain.customer.customer_entities import Customer
from kiki_delivery.domain.shared.repository import AbcFullGenericRepository


class AbcCustomerRepository(AbcFullGenericRepository[Customer]):
    ...
