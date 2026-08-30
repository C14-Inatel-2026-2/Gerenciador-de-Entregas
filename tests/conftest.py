"""Fixtures compartilhadas entre todos os testes."""

import pytest


@pytest.fixture
def motorista_valido():
    # TODO: devolver um Motorista com CNH válida e disponível
    ...


@pytest.fixture
def veiculo_padrao():
    # TODO: devolver um Veiculo disponível, com capacidade e consumo definidos
    ...


@pytest.fixture
def entregas():
    # TODO: devolver uma lista de Entrega com coordenadas conhecidas
    ...


@pytest.fixture
def mapas_falso(mocker):
    """Mock do ProvedorMapas, com matriz de distâncias fixa."""
    from gestao_frotas.interfaces.provedor_mapas import ProvedorMapas

    mock = mocker.Mock(spec=ProvedorMapas)
    mock.matriz_distancias.return_value = [
        [0.0, 10.0, 20.0],
        [10.0, 0.0, 15.0],
        [20.0, 15.0, 0.0],
    ]
    return mock


@pytest.fixture
def combustivel_falso(mocker):
    """Mock do ProvedorCombustivel, com preço fixo."""
    from gestao_frotas.interfaces.provedor_combustivel import ProvedorCombustivel

    mock = mocker.Mock(spec=ProvedorCombustivel)
    mock.preco_por_litro.return_value = 6.00
    return mock
