import pytest

from gestao_frotas.modelos.veiculo import Veiculo


def test_criar_veiculo():
    veiculo = Veiculo(
        1,
        "1234ABC",
        "Volvo",
        12000,
        4.5,
        2.80,
        "caminhão"
    )

    assert veiculo.id == 1
    assert veiculo.placa == "1234ABC"
    assert veiculo.modelo == "Volvo"
    assert veiculo.capacidade_de_carga == 12000
    assert veiculo.consumo_medio == 4.5
    assert veiculo.custo_por_km == 2.80
    assert veiculo.tipo == "caminhão"


def test_veiculo_com_propriedade_somente_leitura():
    veiculo = Veiculo(
        1, "1234ABC", "Volvo", 12000, 4.5, 2.80, "caminhão"
    )

    with pytest.raises(AttributeError):
        veiculo.placa = "5678DEF"


def test_veiculo_com_modelo_mock(mocker):
    modelo = mocker.Mock()

    veiculo = Veiculo(
        1, "1234ABC", modelo, 12000, 4.5, 2.80, "caminhão"
    )

    assert veiculo.modelo is modelo


def test_veiculo_com_tipo_mock(mocker):
    tipo = mocker.Mock()

    veiculo = Veiculo(
        1, "1234ABC", "Volvo", 12000, 4.5, 2.80, tipo
    )

    assert veiculo.tipo is tipo

