from dataclasses import dataclass
from typing import Optional
from kiki_delivery.domain.product.product_value_objects import ProductCategory, Price


@dataclass
class Product:
    name: str
    category: ProductCategory
    price: Price
    description: str = ""
    picture: str = ""
    id: Optional[int] = None
