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

        if not entregas:
            return []

        if hasattr(self.provedor_mapas, "construir_grafo_para_viagem"):
            cidades_viagem = [origem_atual] + [e.origem for e in entregas] + [e.destino for e in entregas]
            self.provedor_mapas.construir_grafo_para_viagem(cidades_viagem)

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

        vetor_final = []
        for i in range(len(entregas_otimizadas)):
            vetor_final.append(entregas_otimizadas[i])
            if i < len(entregas_otimizadas) - 1:
                destino_atual = entregas_otimizadas[i].destino
                proxima_origem = entregas_otimizadas[i + 1].origem
                if destino_atual != proxima_origem and proxima_origem != "Base":
                    entrega_meio = Entrega(
                        0,
                        destino_atual,
                        proxima_origem,
                        1.0
                    )
                    vetor_final.append(entrega_meio)

        return vetor_final