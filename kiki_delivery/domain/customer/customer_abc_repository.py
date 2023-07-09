from typing import overload, List
from .customer_entities import Customer
from ..shared.repository import AbcFullGenericRepository


class AbcCustomerRepository(AbcFullGenericRepository[Customer]):
    ...
