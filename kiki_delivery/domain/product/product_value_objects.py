from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN, InvalidOperation
from kiki_delivery.domain.shared.exceptions import DomainValidatorException


@dataclass(frozen=True)
class ProductCategory:
    value: str

    def __post_init__(self):
        if self.value not in PRODUCT_CATEGORIES_OPTIONS:
            raise DomainValidatorException("Unavailable product category.")


PRODUCT_CATEGORIES_OPTIONS = (
    "SNACK",
    "SIDE",
    "DRINK",
    "DESSERT",
)


@dataclass(init=False)
class Price:
    value: Decimal

    def __init__(self, value: str):
        try:
            self.value = Decimal(value).quantize(Decimal(".01"), rounding=ROUND_DOWN)
        except InvalidOperation:
            raise DomainValidatorException("Invalid decimal value format.")

    def __post_init__(self):
        if self.value < 0:
            raise DomainValidatorException("Price can't be negative.")
