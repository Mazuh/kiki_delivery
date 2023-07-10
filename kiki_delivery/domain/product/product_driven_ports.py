import abc
from typing import List, Optional
from kiki_delivery.domain.product.product_entities import Product, ProductCategory
from kiki_delivery.domain.shared.repository import AbcFullGenericRepository


class AbcProductRepository(AbcFullGenericRepository[Product]):
    ...

    @abc.abstractmethod
    def list(self, category: Optional[ProductCategory] = None) -> List[Product]:
        raise NotImplementedError
