"""Testes unitários do modelo Motorista."""

import pytest

from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.excecoes import StatusInvalidoException


def test_criar_motorista_comeca_disponivel_por_padrao():
    motorista = Motorista(1, "Leo", "12345678900")

    assert motorista.id == 1
    assert motorista.nome == "Leo"
    assert motorista.cnh == "12345678900"
    assert motorista.status == Motorista.STATUS_DISPONIVEL


def test_criar_motorista_com_status_invalido_lanca_value_error():
    with pytest.raises(ValueError):
        Motorista(1, "Leo", "123", status="dormindo")


@pytest.mark.parametrize(
    "novo_status",
    [Motorista.STATUS_EM_VIAGEM, Motorista.STATUS_INDISPONIVEL, Motorista.STATUS_DISPONIVEL],
)
def test_setter_aceita_todos_os_status_validos(novo_status):
    motorista = Motorista(1, "Leo", "123")

    motorista.status = novo_status

    assert motorista.status == novo_status


def test_setter_com_status_invalido_lanca_excecao():
    motorista = Motorista(1, "Leo", "123")

    with pytest.raises(StatusInvalidoException):
        motorista.status = "de ferias"
