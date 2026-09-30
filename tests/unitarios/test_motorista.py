import pytest
from gestao_frotas.modelos.motorista import Motorista


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