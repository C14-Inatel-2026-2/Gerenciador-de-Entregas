from gestao_frotas.excecoes import DadoInvalidoException
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.interfaces.provedor_mapas import ProvedorMapas


class OtimizadorRotas:

    def __init__(self, provedor_mapas: ProvedorMapas):
        self.provedor_mapas = provedor_mapas

    def processar_rota(self, origem: str, destino: str) -> Rota:
        if not origem or not origem.strip():
            raise DadoInvalidoException("A origem informada é vazia ou inválida.")

        if not destino or not destino.strip():
            raise DadoInvalidoException("O destino informado é vazio ou inválido.")

        distancia_km, tempo_estimado_horas = self.provedor_mapas.calcular_distancia_e_tempo(origem, destino)

        return Rota(origem, destino, distancia_km, tempo_estimado_horas)

    def otimizar_entregas(self, entregas: list[Entrega]) -> list[Entrega]:
        return sorted(entregas, key=lambda entrega: entrega.get_prioridade().value, reverse=True)