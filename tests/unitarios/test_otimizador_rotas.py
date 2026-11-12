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

def test_processar_rota_com_sucesso(otimizador):
    rota = otimizador.processar_rota("Santa Rita", "Pouso Alegre")
    assert rota.origem == "Santa Rita"
    assert rota.destino == "Pouso Alegre"
    assert rota.distancia_km == 50.0
    assert rota.tempo_estimado_horas == 1.0

def test_origem_vazia_deve_lancar_excecao(otimizador):
    with pytest.raises(DadoInvalidoException):
        otimizador.processar_rota("", "Pouso Alegre")

def test_destino_vazio_deve_lancar_excecao(otimizador):
    with pytest.raises(DadoInvalidoException):
        otimizador.processar_rota("Santa Rita", "   ")


def test_otimizar_entregas_ordena_por_prioridade(otimizador):
    entrega_baixa = Entrega(1, "A", "B", 10.0, Prioridade.BAIXA)
    entrega_alta = Entrega(2, "C", "D", 5.0, Prioridade.ALTA)
    entrega_normal = Entrega(3, "E", "F", 2.0, Prioridade.NORMAL)

    entregas = [entrega_baixa, entrega_alta, entrega_normal]
    entregas_otimizadas = otimizador.otimizar_entregas(entregas)

    assert entregas_otimizadas[0].get_prioridade() == Prioridade.ALTA
    assert entregas_otimizadas[1].get_prioridade() == Prioridade.NORMAL
    assert entregas_otimizadas[2].get_prioridade() == Prioridade.BAIXA