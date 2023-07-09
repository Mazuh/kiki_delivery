from typing import Self
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from kiki_delivery.domain.product import Product, ProductCategory, Price
from kiki_delivery.infrastructure.shared.database import Base


class ProductORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    category: Mapped[str] = mapped_column(String(30), nullable=False)
    price: Mapped[str] = mapped_column(String(10), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False, default="")
    picture: Mapped[str] = mapped_column(String(300), nullable=False, default="")

    def to_entity(self) -> Product:
        return Product(
            id=self.id,
            name=self.name,
            category=ProductCategory(self.category),
            price=Price(self.price),
            description=self.description,
            picture=self.picture,
        )

    @classmethod
    def from_entity(cls, product: Product) -> Self:
        return cls(
            id=product.id,
            name=product.name,
            category=product.category.value,
            price=product.price.value.to_eng_string(),
            description=product.description,
            picture=product.picture,
        )
