from gestao_frotas.excecoes import DadoInvalidoException
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.interfaces.provedor_mapas import ProvedorMapas


class OtimizadorRotas:

    def __init__(self, provedor_mapas: ProvedorMapas):
        self.provedor_mapas = provedor_mapas

    def processar_rota(self, origem: str, destino: str) -> Rota:
        if not origem.strip():
            raise DadoInvalidoException("A origem informada é vazia ou inválida.")

        if not destino.strip():
            raise DadoInvalidoException("O destino informado é vazio ou inválido.")

        distancia_km, tempo_estimado_horas = self.provedor_mapas.calcular_distancia_e_tempo(origem, destino)
        return Rota(origem, destino, distancia_km, tempo_estimado_horas)

    def otimizar_entregas(self, origem_atual: str, entregas: list[Entrega]) -> list[Entrega]:
        """Calcula a sequência de entregas baseada na menor distância (Vizinho Mais Próximo)"""
        entregas_pendentes = entregas.copy()
        entregas_otimizadas = []
        local_atual = origem_atual

        while entregas_pendentes:
            proxima_entrega = None
            menor_distancia = float('inf')

            for entrega in entregas_pendentes:
                distancia, _ = self.provedor_mapas.calcular_distancia_e_tempo(local_atual, entrega.destino)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    proxima_entrega = entrega

            entregas_otimizadas.append(proxima_entrega)
            entregas_pendentes.remove(proxima_entrega)
            local_atual = proxima_entrega.destino

        return entregas_otimizadas

    def preparar_viagem(self, origem: str, destino: str, entregas: list[Entrega]) -> tuple[Rota, list[Entrega]]:
        rota = self.processar_rota(origem, destino)
        entregas_otimizadas = self.otimizar_entregas(origem,entregas)
        return rota, entregas_otimizadas