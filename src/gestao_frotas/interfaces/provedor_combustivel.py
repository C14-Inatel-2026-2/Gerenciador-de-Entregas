from abc import ABC, abstractmethod


class ProvedorCombustivel(ABC):

    @abstractmethod
    def preco_por_litro(self, uf: str) -> float:
        ...
