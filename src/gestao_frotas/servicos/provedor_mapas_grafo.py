import networkx as nx
from gestao_frotas.interfaces.provedor_mapas import ProvedorMapas


class ProvedorMapasGrafo(ProvedorMapas):
    def __init__(self):
        self.grafo = nx.Graph()

        self.grafo.add_edge("Santa Rita do Sapucaí", "Pouso Alegre", distancia=25.0, tempo=0.5)
        self.grafo.add_edge("Pouso Alegre", "Borda da Mata", distancia=20.0, tempo=0.4)
        self.grafo.add_edge("Santa Rita do Sapucaí", "Itajubá", distancia=45.0, tempo=0.8)
        self.grafo.add_edge("Pouso Alegre", "Itajubá", distancia=60.0, tempo=1.0)
        self.grafo.add_edge("Itajubá", "Maria da Fé", distancia=30.0, tempo=0.6)

    def calcular_distancia_e_tempo(self, origem: str, destino: str) -> tuple[float, float]:
        if origem not in self.grafo or destino not in self.grafo:
            return 50.0, 1.0

        try:
            caminho = nx.shortest_path(self.grafo, source=origem, target=destino, weight="distancia")
            distancia = nx.path_weight(self.grafo, caminho, weight="distancia")
            tempo = nx.path_weight(self.grafo, caminho, weight="tempo")
            return distancia, tempo
        except nx.NetworkXNoPath:
            return 999.0, 99.0