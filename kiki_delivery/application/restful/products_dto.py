from typing import Self, List
from dataclasses import dataclass
from kiki_delivery.application.restful.shared import dto
from kiki_delivery.domain.product.product_entities import Product
from kiki_delivery.domain.product.product_value_objects import ProductCategory, Price


class ProductPostDTO(dto.RESTfulInputDTO[Product]):
    name: str
    category: str
    price: str
    description: str
    picture: str

    def to_entity(self):
        return Product(
            name=self.name,
            category=ProductCategory(self.category),
            price=Price(self.price),
            description=self.description,
            picture=self.picture,
        )


class ProductPutDTO(dto.RESTfulInputDTO[Product]):
    id: int
    name: str
    category: str
    price: str
    description: str
    picture: str

    def to_entity(self) -> Product:
        return Product(
            id=self.id,
            name=self.name,
            category=ProductCategory(self.category),
            price=Price(self.price),
            description=self.description,
            picture=self.picture,
        )


@dataclass
class ProductDTO(dto.RESTfulItemDTO[Product]):
    id: int
    name: str
    category: str
    price: str
    description: str
    picture: str

    @classmethod
    def from_entity(cls, product: Product) -> Self:
        return cls(
            id=product.id or -1,
            name=product.name,
            category=product.category.value,
            price=product.price.value.to_eng_string(),
            description=product.description,
            picture=product.picture,
        )


class ProductsDTO(dto.RESTfulCollectionDTO[Product, ProductDTO]):
    @classmethod
    def from_entities(cls, products: List[Product]):
        return cls(items=[ProductDTO.from_entity(it) for it in products])
