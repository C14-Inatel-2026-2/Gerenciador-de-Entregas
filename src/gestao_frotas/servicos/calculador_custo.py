"""Cálculo do custo de uma rota.

Custo = (distancia / consumo) * preco_combustivel
      + pedagios
      + horas_estimadas * custo_hora_motorista
"""

from gestao_frotas.interfaces.provedor_combustivel import ProvedorCombustivel


class CalculadorCusto:
    def __init__(self, provedor_combustivel: ProvedorCombustivel) -> None:
        self._combustivel = provedor_combustivel

    # TODO: calcular(rota, veiculo, motorista) -> float
