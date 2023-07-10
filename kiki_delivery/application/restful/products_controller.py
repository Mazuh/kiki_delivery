from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from kiki_delivery.application.restful.products_dto import (
    ProductDTO,
    ProductsDTO,
    ProductPostDTO,
    ProductPutDTO,
)
from kiki_delivery.domain.product import AbcProductRepository, ProductCategory
from kiki_delivery.infrastructure.repositories.product_repository import (
    ProductRepository,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_product(
    product_dto: ProductPostDTO,
    product_repo: AbcProductRepository = Depends(ProductRepository),
):
    product = product_dto.to_entity()
    created = product_repo.create(product)
    return ProductDTO.from_entity(created)


@router.get("/")
async def get_products(
    product_repo: AbcProductRepository = Depends(ProductRepository),
    category: Annotated[str, Query()] = "",
):
    products = product_repo.list(
        category=ProductCategory(category) if category else None
    )
    return ProductsDTO.from_entities(products)


@router.get("/categories")
async def get_product_categories():
    return ProductCategory.get_options()


@router.get("/{id}")
async def get_product(
    id: int,
    response: Response,
    product_repo: AbcProductRepository = Depends(ProductRepository),
):
    product = product_repo.read(id)
    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return ProductDTO.from_entity(product)


@router.put("/{id}")
async def put_product(
    id: int,
    response: Response,
    product_dto: ProductPutDTO,
    product_repo: AbcProductRepository = Depends(ProductRepository),
):
    product = product_dto.to_entity()

    updated = product_repo.update(id, product)
    if not updated:
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    return ProductDTO.from_entity(updated)


@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_product(
    id: int,
    product_repo: AbcProductRepository = Depends(ProductRepository),
):
    product_repo.delete(id)
    return dict(id=id)
