"""Montagem de rotas otimizadas.

Recebe um ProvedorMapas por injeção de dependência.
Heurística sugerida: vizinho mais próximo + refino 2-opt.
"""

from gestao_frotas.interfaces.provedor_mapas import ProvedorMapas


class OtimizadorRotas:
    def __init__(self, provedor_mapas: ProvedorMapas) -> None:
        self._mapas = provedor_mapas

    # TODO: otimizar(entregas) -> Rota
