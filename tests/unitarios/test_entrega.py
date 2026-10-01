"""Testes unitários do modelo Entrega."""

import pytest

from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.excecoes import DadoInvalidoException, StatusInvalidoException


def test_criar_entrega_valida_guarda_os_atributos():
    entrega = Entrega(1, "Santa Rita", "Pouso Alegre", 10.5, "Alta")

    assert entrega.id == 1
    assert entrega.origem == "Santa Rita"
    assert entrega.destino == "Pouso Alegre"
    assert entrega.peso == 10.5
    assert entrega.prioridade == "Alta"
    assert entrega.status == "Pendente"  # valor padrão


def test_prioridade_e_status_tem_valores_padrao():
    entrega = Entrega(2, "A", "B", 1)

    assert entrega.prioridade == "Normal"
    assert entrega.status == "Pendente"


@pytest.mark.parametrize("peso_invalido", [0, -1, -10.5])
def test_peso_menor_ou_igual_a_zero_lanca_excecao(peso_invalido):
    with pytest.raises(DadoInvalidoException):
        Entrega(1, "A", "B", peso_invalido)


def test_prioridade_invalida_lanca_excecao():
    with pytest.raises(DadoInvalidoException):
        Entrega(1, "A", "B", 5, prioridade="Urgentissima")


def test_status_inicial_invalido_lanca_excecao():
    with pytest.raises(StatusInvalidoException):
        Entrega(1, "A", "B", 5, status="Sumiu")


def test_alterar_prioridade_valida():
    entrega = Entrega(1, "A", "B", 5, prioridade="Normal")

    entrega.alterar_prioridade("Alta")

    assert entrega.prioridade == "Alta"


def test_alterar_prioridade_invalida_lanca_excecao():
    entrega = Entrega(1, "A", "B", 5)

    with pytest.raises(DadoInvalidoException):
        entrega.alterar_prioridade("Media")


def test_atualizar_status_valido():
    entrega = Entrega(1, "A", "B", 5)

    entrega.atualizar_status("A Caminho")
    assert entrega.status == "A Caminho"

    entrega.atualizar_status("Entregue")
    assert entrega.status == "Entregue"


def test_atualizar_status_invalido_lanca_excecao():
    entrega = Entrega(1, "A", "B", 5)

    with pytest.raises(StatusInvalidoException):
        entrega.atualizar_status("Perdida")
