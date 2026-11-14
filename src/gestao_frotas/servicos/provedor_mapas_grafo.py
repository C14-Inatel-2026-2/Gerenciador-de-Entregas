import json
import math
import urllib.parse
import urllib.request
import networkx as nx
from gestao_frotas.interfaces.provedor_mapas import ProvedorMapas


class ProvedorMapasGrafo(ProvedorMapas):
    def __init__(self):
        self.grafo = nx.Graph()
        self.cache_coordenadas: dict[str, tuple[float, float]] = {}

        # Malha base (mantém os testes atuais funcionando)
        self.grafo.add_edge("Santa Rita do Sapucaí", "Pouso Alegre", distancia=25.0, tempo=0.5)
        self.grafo.add_edge("Pouso Alegre", "Borda da Mata", distancia=20.0, tempo=0.4)
        self.grafo.add_edge("Santa Rita do Sapucaí", "Itajubá", distancia=45.0, tempo=0.8)
        self.grafo.add_edge("Pouso Alegre", "Itajubá", distancia=60.0, tempo=1.0)
        self.grafo.add_edge("Itajubá", "Maria da Fé", distancia=30.0, tempo=0.6)

    def obter_coordenadas(self, endereco: str) -> tuple[float, float] | None:
        if endereco in self.cache_coordenadas:
            return self.cache_coordenadas[endereco]

        termo = urllib.parse.quote(endereco)
        url = f"https://nominatim.openstreetmap.org/search?q={termo}&format=json&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "GerenciadorDeEntregasInatel/1.0"})

        try:
            with urllib.request.urlopen(req, timeout=5) as resposta:
                dados = json.loads(resposta.read().decode())
                if dados:
                    coords = (float(dados[0]["lat"]), float(dados[0]["lon"]))
                    self.cache_coordenadas[endereco] = coords
                    return coords
        except Exception:
            pass
        return None

    def buscar_trajeto_osrm(self, coord_origem: tuple[float, float], coord_destino: tuple[float, float]) -> tuple[float, float] | None:
        url = (
            "https://router.project-osrm.org/route/v1/driving/"
            f"{coord_origem[1]},{coord_origem[0]};"
            f"{coord_destino[1]},{coord_destino[0]}"
            "?overview=false"
        )
        try:
            with urllib.request.urlopen(url, timeout=5) as resposta:
                dados = json.loads(resposta.read().decode())
            if dados.get("code") == "Ok" and dados.get("routes"):
                rota = dados["routes"][0]
                distancia_km = round(rota["distance"] / 1000.0, 2)
                tempo_horas = round(rota["duration"] / 3600.0, 2)
                return distancia_km, max(tempo_horas, 0.1)
        except Exception:
            pass
        return None

    def distancia_em_linha_reta(self, coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
        raio_terra_km = 6371.0
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return round(2 * raio_terra_km * math.asin(math.sqrt(a)), 2)

    def adicionar_conexao_dinamica(self, origem: str, destino: str) -> bool:
        if origem == destino:
            return True
        if self.grafo.has_edge(origem, destino):
            return True

        coord_origem = self.obter_coordenadas(origem)
        coord_destino = self.obter_coordenadas(destino)

        if not coord_origem or not coord_destino:
            return False

        resultado_osrm = self.buscar_trajeto_osrm(coord_origem, coord_destino)
        if resultado_osrm is not None:
            distancia, tempo = resultado_osrm
        else:
            distancia = self.distancia_em_linha_reta(coord_origem, coord_destino)
            tempo = round(distancia / 60.0, 2)

        self.grafo.add_edge(origem, destino, distancia=distancia, tempo=tempo)
        return True

    def construir_grafo_para_viagem(self, cidades: list[str]):
        cidades_unicas = list(dict.fromkeys(c.strip() for c in cidades if c and c.strip()))
        for i in range(len(cidades_unicas)):
            for j in range(i + 1, len(cidades_unicas)):
                self.adicionar_conexao_dinamica(cidades_unicas[i], cidades_unicas[j])

    def calcular_distancia_e_tempo(self, origem: str, destino: str) -> tuple[float, float]:
        if origem == destino:
            return 0.0, 0.0

        if origem not in self.grafo or destino not in self.grafo or not nx.has_path(self.grafo, origem, destino):
            conectou = self.adicionar_conexao_dinamica(origem, destino)
            if not conectou and (origem not in self.grafo or destino not in self.grafo):
                return 50.0, 1.0

        try:
            caminho = nx.shortest_path(self.grafo, source=origem, target=destino, weight="distancia")
            distancia = nx.path_weight(self.grafo, caminho, weight="distancia")
            tempo = nx.path_weight(self.grafo, caminho, weight="tempo")
            return distancia, tempo
        except nx.NetworkXNoPath:
            return 999.0, 99.0