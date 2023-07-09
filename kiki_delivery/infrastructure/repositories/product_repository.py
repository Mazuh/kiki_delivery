from typing import Optional, List
from kiki_delivery.domain.product import AbcProductRepository, Product
from kiki_delivery.infrastructure.shared.db_repository import AbcDatabaseRepository
from kiki_delivery.infrastructure.orm.product_orm import ProductORM


class ProductRepository(AbcDatabaseRepository, AbcProductRepository):
    def create(self, product: Product) -> Product:
        product_orm = ProductORM.from_entity(product)
        self._session.add(product_orm)
        self._session.commit()
        self._session.refresh(product_orm)
        return product_orm.to_entity()

    def read(self, id: int) -> Optional[Product]:
        product_orm = (
            self._session.query(ProductORM).filter(ProductORM.id == id).first()
        )
        return product_orm.to_entity() if product_orm else None

    def list(self) -> List[Product]:
        products_orm = self._session.query(ProductORM).all()
        return [c.to_entity() for c in products_orm]

    def update(self, id: int, product: Product) -> Optional[Product]:
        existing = self._session.query(ProductORM).filter(ProductORM.id == id).first()
        if existing is None:
            return None

        updating = ProductORM.from_entity(product)

        for key, value in updating.__dict__.items():
            if not key.startswith("_") and key != "id" and value is not None:
                setattr(existing, key, value)

        self._session.commit()
        self._session.refresh(existing)

        return existing.to_entity()

    def delete(self, id: int) -> None:
        product = self._session.query(ProductORM).filter(ProductORM.id == id).first()
        if product is None:
            return

        self._session.delete(product)
        self._session.commit()
