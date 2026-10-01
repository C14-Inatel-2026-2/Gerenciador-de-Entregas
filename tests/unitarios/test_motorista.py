import pytest
from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.modelos.veiculo import Veiculo


def test_motorista_com_cnh():
    cnh = {
        "12345678900": ["carro", "caminhão"]
    }

    motorista = Motorista(1, "Gabriel", cnh)

    assert motorista.cnh == cnh


def test_atualizar_status_motorista():
    motorista = Motorista(1, "Gabriel", {})

    motorista.atualizar_status("em viagem")

    assert motorista.status == "em viagem"


def test_atualizar_status_invalido():
    motorista = Motorista(1, "Gabriel", {})

    with pytest.raises(ValueError):
        motorista.atualizar_status("dirigindo")


def test_atribuir_veiculo_permitido(mocker):
    cnh = {
        "12345678900": ["carro"]
    }

    motorista = Motorista(1, "Gabriel", cnh)

    veiculo = mocker.Mock(spec=Veiculo)
    veiculo.tipo = "carro"

    motorista.atribuir_veiculo(veiculo)

    assert motorista.veiculo == veiculo


def test_atribuir_veiculo_nao_permitido(mocker):
    cnh = {
        "12345678900": ["carro"]
    }

    motorista = Motorista(1, "Gabriel", cnh)

    veiculo = mocker.Mock(spec=Veiculo)
    veiculo.tipo = "caminhão"

    with pytest.raises(ValueError):
        motorista.atribuir_veiculo(veiculo)