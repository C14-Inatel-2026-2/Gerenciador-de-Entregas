import pytest
from unittest.mock import Mock
from gestao_frotas.servicos.otimizador_rotas import OtimizadorRotas
from gestao_frotas.modelos.entrega import Entrega, Prioridade
from gestao_frotas.excecoes import DadoInvalidoException


@pytest.fixture
def provedor_mock():
    mock = Mock()

    def distancias_simuladas(origem, destino):

        tabela = {
            ("Santa Rita", "Pouso Alegre"): (25.0, 0.5),
            ("Santa Rita", "Cachoeira de Minas"): (30.0, 0.6),
            ("Santa Rita", "Itajubá"): (45.0, 0.8),
            ("Pouso Alegre", "Borda da Mata"): (20.0, 0.4),
            ("Pouso Alegre", "Cachoeira de Minas"): (25.0, 0.5),
            ("Pouso Alegre", "Itajubá"): (60.0, 1.0),
            ("Borda da Mata", "Cachoeira de Minas"): (15.0, 0.3),
            ("Borda da Mata", "Itajubá"): (70.0, 1.2),
            ("Cachoeira de Minas", "Itajubá"): (40.0, 0.7),
            ("Itajubá", "Maria da Fé"): (30.0, 0.6)
        }

        if (origem, destino) in tabela: return tabela[(origem, destino)]
        if (destino, origem) in tabela: return tabela[(destino, origem)]
        return (999.0, 99.0)

    mock.calcular_distancia_e_tempo.side_effect = distancias_simuladas
    return mock


@pytest.fixture
def otimizador(provedor_mock):
    return OtimizadorRotas(provedor_mock)


def test_processar_rota_com_sucesso(otimizador, provedor_mock):
    rota = otimizador.processar_rota("Santa Rita", "Pouso Alegre")
    assert rota.origem == "Santa Rita"
    assert rota.destino == "Pouso Alegre"
    assert rota.distancia_km == 25.0


def test_origem_vazia_deve_lancar_excecao(otimizador):
    with pytest.raises(DadoInvalidoException):
        otimizador.processar_rota("", "Pouso Alegre")


def test_destino_vazio_deve_lancar_excecao(otimizador):
    with pytest.raises(DadoInvalidoException):
        otimizador.processar_rota("Santa Rita", "   ")


def test_otimizar_entregas_complexa_com_cinco_cidades(otimizador):

    entrega1 = Entrega(1, "Base", "Maria da Fé", 10.0)
    entrega2 = Entrega(2, "Base", "Itajubá", 15.0)
    entrega3 = Entrega(3, "Base", "Borda da Mata", 5.0)
    entrega4 = Entrega(4, "Base", "Cachoeira de Minas", 8.0)
    entrega5 = Entrega(5, "Base", "Pouso Alegre", 20.0)

    entregas = [entrega1, entrega2, entrega3, entrega4, entrega5]


    sequencia = otimizador.otimizar_entregas("Santa Rita", entregas)


    assert sequencia[0].destino == "Pouso Alegre"
    assert sequencia[1].destino == "Borda da Mata"
    assert sequencia[2].destino == "Cachoeira de Minas"
    assert sequencia[3].destino == "Itajubá"
    assert sequencia[4].destino == "Maria da Fé"

def test_otimizar_entregas_insere_deslocamento_quando_ha_salto(otimizador):
    entrega1 = Entrega(1, "Santa Rita", "Pouso Alegre", 10.0)
    entrega2 = Entrega(2, "Itajubá", "Maria da Fé", 15.0)

    sequencia = otimizador.otimizar_entregas("Santa Rita", [entrega1, entrega2])


    assert len(sequencia) == 3
    assert sequencia[0].origem == "Santa Rita"
    assert sequencia[0].destino == "Pouso Alegre"

    assert sequencia[1].id == 0
    assert sequencia[1].origem == "Pouso Alegre"
    assert sequencia[1].destino == "Itajubá"

    assert sequencia[2].origem == "Itajubá"
    assert sequencia[2].destino == "Maria da Fé"