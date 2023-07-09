from kiki_delivery.domain.product.product_entities import Product
from kiki_delivery.domain.shared.repository import AbcFullGenericRepository


class AbcProductRepository(AbcFullGenericRepository[Product]):
    ...
