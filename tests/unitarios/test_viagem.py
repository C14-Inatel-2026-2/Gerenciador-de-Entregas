"""Testes unitários do modelo Viagem."""

import pytest

from gestao_frotas.modelos.viagem import Viagem
from gestao_frotas.excecoes import StatusInvalidoException


def test_criar_viagem_valida_guarda_os_atributos():
    viagem = Viagem("motorista", "veiculo", "rota", ["entrega1", "entrega2"])

    assert viagem.motorista == "motorista"
    assert viagem.veiculo == "veiculo"
    assert viagem.rota == "rota"
    assert viagem.entregas == ["entrega1", "entrega2"]
    assert viagem.status == "Pendente"  # valor padrão


def test_entregas_none_vira_lista_vazia():
    viagem = Viagem("m", "v", "r", None)

    assert viagem.entregas == []


def test_status_inicial_invalido_lanca_excecao():
    with pytest.raises(StatusInvalidoException):
        Viagem("m", "v", "r", [], status="Voando")


@pytest.mark.parametrize("novo_status", ["Em Andamento", "Concluida"])
def test_atualizar_status_valido(novo_status):
    viagem = Viagem("m", "v", "r", [])

    viagem.atualizar_status(novo_status)

    assert viagem.status == novo_status


def test_atualizar_status_invalido_lanca_excecao():
    viagem = Viagem("m", "v", "r", [])

    with pytest.raises(StatusInvalidoException):
        viagem.atualizar_status("Cancelada")
