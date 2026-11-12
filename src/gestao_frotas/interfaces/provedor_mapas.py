from abc import ABC, abstractmethod

class ProvedorMapas(ABC):

    @abstractmethod
    def calcular_distancia_e_tempo(self, origem: str, destino: str) -> tuple[float, float]:
        ...
