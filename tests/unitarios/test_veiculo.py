"""Testes unitários do modelo Veiculo."""

import pytest

from gestao_frotas.modelos.veiculo import Veiculo


def criar_veiculo(capacidade=1000):
    return Veiculo(
        id=1,
        placa="ABC1D23",
        modelo="Fiorino",
        capacidade_de_carga=capacidade,
        consumo_medio=12.0,
        custo_por_km=1.5,
    )


def test_getters_guardam_os_valores_do_construtor():
    veiculo = criar_veiculo()

    assert veiculo.id == 1
    assert veiculo.placa == "ABC1D23"
    assert veiculo.modelo == "Fiorino"
    assert veiculo.capacidade_de_carga == 1000
    assert veiculo.consumo_medio == 12.0
    assert veiculo.custo_por_km == 1.5


def test_pode_transportar_peso_abaixo_da_capacidade():
    veiculo = criar_veiculo(capacidade=1000)

    assert veiculo.pode_transportar(800) is True


def test_pode_transportar_peso_igual_a_capacidade():
    veiculo = criar_veiculo(capacidade=1000)

    assert veiculo.pode_transportar(1000) is True


def test_nao_pode_transportar_peso_acima_da_capacidade():
    veiculo = criar_veiculo(capacidade=1000)

    assert veiculo.pode_transportar(1200) is False
