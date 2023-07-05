import re
from dataclasses import dataclass
from kiki_delivery.domain.shared.exceptions import DomainValidatorException


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise DomainValidatorException("Invalid email.")


@dataclass(frozen=True)
class Cpf:
    value: str

    def __post_init__(self):
        cpf_regex = re.compile(r"(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})")
        if not cpf_regex.fullmatch(self.value):
            raise DomainValidatorException("Invalid CPF, not enough digits.")
