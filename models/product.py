"""Produto do catálogo, com preço representado em centavos inteiros."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    identifier: int
    name: str
    price_cents: int

    def __post_init__(self) -> None:
        if type(self.identifier) is not int or self.identifier <= 0:
            raise ValueError("O identificador deve ser um inteiro positivo.")
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("O nome do produto não pode ser vazio.")
        if type(self.price_cents) is not int or self.price_cents < 0:
            raise ValueError("O preço deve ser um inteiro não negativo em centavos.")

    @property
    def formatted_price(self) -> str:
        reais, centavos = divmod(self.price_cents, 100)
        return f"R$ {reais:,}".replace(",", ".") + f",{centavos:02d}"
