import unittest
from sqlalchemy import text
from fastapi.testclient import TestClient
from kiki_delivery.application.web import app
from kiki_delivery.domain.product.product_entities import Product
from kiki_delivery.domain.product.product_value_objects import ProductCategory, Price
from kiki_delivery.domain.product.product_abc_repository import AbcProductRepository
from kiki_delivery.infrastructure.repositories.product_repository import (
    ProductRepository,
)


class TestProducts(unittest.TestCase):
    def setUp(self):
        self.product_repo = ProductRepository()

        self.snack = self.product_repo.create(
            Product(
                name="Sanduiche",
                category=ProductCategory("SNACK"),
                price=Price("2.50"),
            )
        )
        self.side = self.product_repo.create(
            Product(
                name="Salada Caesar",
                category=ProductCategory("SIDE"),
                price=Price("4.99"),
            )
        )
        self.drink = self.product_repo.create(
            Product(
                name="Suco de Laranja",
                category=ProductCategory("DRINK"),
                price=Price("1.00"),
            )
        )
        self.dessert = self.product_repo.create(
            Product(
                name="Brigadeiro",
                category=ProductCategory("DESSERT"),
                price=Price("0.50"),
            )
        )

        app.dependency_overrides[AbcProductRepository] = lambda: self.product_repo
        self.client = TestClient(app)

    def tearDown(self):
        self.product_repo.delete(self.snack.id)  # type: ignore
        self.product_repo.delete(self.side.id)  # type: ignore
        self.product_repo.delete(self.drink.id)  # type: ignore
        self.product_repo.delete(self.dessert.id)  # type: ignore
        self.product_repo._session.close()

    def test_post_product(self):
        post_data = {
            "name": "Gelatina",
            "category": "DESSERT",
            "price": "0.99",
            "description": "",
            "picture": "",
        }
        response = self.client.post("/products/", json=post_data)
        assert response.status_code == 201

        response_data = response.json()
        created_id = response_data.pop("id")
        assert created_id is not None
        assert response_data == {
            "name": "Gelatina",
            "category": "DESSERT",
            "price": "0.99",
            "description": "",
            "picture": "",
        }

        self.product_repo.delete(created_id)

    def test_get_products(self):
        response = self.client.get("/products/")
        assert response.status_code == 200

        response_data = response.json()
        response_items = response_data["items"]

        assert len(response_items) == 4

    def test_get_product(self):
        response = self.client.get(f"/products/{self.snack.id}")
        assert response.json() == {
            "id": self.snack.id,
            "name": "Sanduiche",
            "category": "SNACK",
            "price": "2.50",
            "description": "",
            "picture": "",
        }

    def test_put_product(self):
        put_data = {
            "id": self.snack.id,
            "name": "Sanduiche (promoção do dia)",
            "category": "SNACK",
            "price": "2.00",
            "description": "",
            "picture": "",
        }
        response = self.client.put(f"/products/{self.snack.id}", json=put_data)
        assert response.status_code == 200
        assert response.json() == put_data

    def test_delete_product(self):
        response = self.client.delete(f"/products/{self.snack.id}")
        assert response.status_code == 202
        assert response.json() == {"id": self.snack.id}

        deleted_id = response.json()["id"]
        assert self.product_repo.read(deleted_id) is None
