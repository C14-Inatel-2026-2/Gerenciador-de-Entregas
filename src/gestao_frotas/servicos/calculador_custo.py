
from gestao_frotas.excecoes import DadoInvalidoException
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.veiculo import Veiculo


class CalculadorCusto:

    def __init__(self, provedor_combustivel):
        self.__provedor = provedor_combustivel

    def litros_necessarios(self, rota: Rota, veiculo: Veiculo) -> float:
        if veiculo.consumo_medio <= 0:
            raise DadoInvalidoException(
                "O consumo médio do veículo deve ser maior que zero."
            )
        return rota.distancia_km / veiculo.consumo_medio

    def custo_por_distancia(self, rota: Rota, veiculo: Veiculo) -> float:
        return rota.distancia_km * veiculo.custo_por_km

    def calcular_custo_combustivel(self, rota: Rota, veiculo: Veiculo, uf: str) -> float:
        litros = self.litros_necessarios(rota, veiculo)
        preco = self.__provedor.preco_por_litro(uf)
        return litros * preco