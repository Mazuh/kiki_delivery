from dataclasses import dataclass
from kiki_delivery.domain.shared.exceptions import DomainValidatorException


@dataclass(frozen=True)
class OrderStatus:
    value: str

    def __post_init__(self):
        if self.value not in OrderStatus.get_options():
            raise DomainValidatorException("Unexisting order status.")

    @staticmethod
    def get_options():
        return (
            "UNCONFIRMED",
            "RECEIVED",
            "IN_PROGRESS",
            "READY",
            "FINISHED",
        )
