import unittest
from sqlalchemy import text
from fastapi.testclient import TestClient
from kiki_delivery.application.web import app
from kiki_delivery.domain.customer.customer_entities import Customer
from kiki_delivery.domain.customer.customer_value_objects import Email, Cpf
from kiki_delivery.domain.customer.customer_abc_repository import AbcCustomerRepository
from kiki_delivery.infrastructure.repositories.customer_repository import (
    CustomerRepository,
)


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.customer_repo = CustomerRepository()

        self.first_customer = self.customer_repo.create(
            Customer(
                first_name="John",
                last_name="Doe",
                cpf=Cpf("111.111.111-11"),
                email=Email("john@doe.com"),
            )
        )
        self.second_customer = self.customer_repo.create(
            Customer(
                first_name="Jane",
                last_name="Doe",
                cpf=Cpf("222.222.222-22"),
                email=Email("jane@doe.com"),
            )
        )

        app.dependency_overrides[AbcCustomerRepository] = lambda: self.customer_repo
        self.client = TestClient(app)

    def tearDown(self):
        self.customer_repo.delete(self.first_customer.id)  # type: ignore
        self.customer_repo.delete(self.second_customer.id)  # type: ignore
        self.customer_repo._session.close()

    def test_post_customer(self):
        post_data = {
            "first_name": "Marcell",
            "last_name": "Guilherme",
            "cpf": "123.123.123-12",
            "email": "marcell@teste.com",
        }
        response = self.client.post("/customers/", json=post_data)
        assert response.status_code == 201

        response_data = response.json()
        created_id = response_data.pop("id")
        assert created_id is not None
        assert response_data == {
            "first_name": "Marcell",
            "last_name": "Guilherme",
            "cpf": "123.123.123-12",
            "email": "marcell@teste.com",
        }

        self.customer_repo.delete(created_id)

    def test_get_customers(self):
        response = self.client.get("/customers/")
        assert response.status_code == 200

        response_data = response.json()
        response_items = response_data["items"]

        assert response_items[0] == {
            "id": self.first_customer.id,
            "cpf": "111.111.111-11",
            "email": "john@doe.com",
            "first_name": "John",
            "last_name": "Doe",
        }

        assert response_items[1] == {
            "id": self.second_customer.id,
            "cpf": "222.222.222-22",
            "email": "jane@doe.com",
            "first_name": "Jane",
            "last_name": "Doe",
        }

    def test_get_customer(self):
        response = self.client.get(f"/customers/{self.second_customer.id}")
        assert response.json() == {
            "id": self.second_customer.id,
            "cpf": "222.222.222-22",
            "email": "jane@doe.com",
            "first_name": "Jane",
            "last_name": "Doe",
        }

    def test_get_customer_not_found(self):
        id = 1234
        response = self.client.get(f"/customers/{id}")
        assert response.status_code == 404

    def test_put_customer(self):
        put_data = {
            "id": self.first_customer.id,
            "first_name": "Marcos",
            "last_name": "Leo",
            "email": "john@doe.com",
            "cpf": "999.999.999-99",
        }
        response = self.client.put(
            f"/customers/{self.first_customer.id}", json=put_data
        )
        assert response.status_code == 200
        assert response.json() == put_data

    def test_put_customer_not_found(self):
        put_data = {
            "id": 666,
            "first_name": "Marcos",
            "last_name": "Leo",
            "email": "john@doe.com",
            "cpf": "999.999.999-99",
        }
        response = self.client.put(
            f"/customers/{self.first_customer.id}", json=put_data
        )
        assert response.status_code == 200

    def test_delete_customer(self):
        response = self.client.delete(f"/customers/{self.first_customer.id}")
        assert response.status_code == 202
        assert response.json() == {"id": self.first_customer.id}
