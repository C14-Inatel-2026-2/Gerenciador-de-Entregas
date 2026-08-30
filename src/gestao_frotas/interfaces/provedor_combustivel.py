"""Contrato de quem fornece o preço do combustível.

Também é substituído por mock nos testes do calculador de custo.
"""

from typing import Protocol


class ProvedorCombustivel(Protocol):
    def preco_por_litro(self, uf: str) -> float:
        ...
