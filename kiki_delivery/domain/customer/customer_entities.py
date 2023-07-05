from dataclasses import dataclass
from typing import Optional
from .customer_value_objects import Email, Cpf


@dataclass
class Customer:
    first_name: str
    last_name: str
    email: Email
    cpf: Cpf
    id: Optional[int] = None
