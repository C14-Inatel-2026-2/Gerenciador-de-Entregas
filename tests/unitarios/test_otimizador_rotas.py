import pytest
from gestao_frotas.servicos.otimizador_rotas import OtimizadorRotas
from gestao_frotas.modelos.entrega import Entrega, Prioridade
from gestao_frotas.excecoes import DadoInvalidoException
from gestao_frotas.interfaces.provedor_mapas import ProvedorMapas

class MockProvedorMapas(ProvedorMapas):
    def calcular_distancia_e_tempo(self, origem: str, destino: str) -> tuple[float, float]:
        return 50.0, 1.0

@pytest.fixture
def otimizador():
    provedor_mock = MockProvedorMapas()
    return OtimizadorRotas(provedor_mapas=provedor_mock)
