"""Contrato de quem fornece distâncias entre pontos.

Nos testes esta interface é substituída por mock (pytest-mock),
então o otimizador nunca depende de chamada de rede.
"""

from typing import Protocol, Sequence


class ProvedorMapas(Protocol):
    def matriz_distancias(
        self, coordenadas: Sequence[tuple[float, float]]
    ) -> list[list[float]]:
        """Retorna a matriz de distâncias em km entre todos os pontos."""
        ...
