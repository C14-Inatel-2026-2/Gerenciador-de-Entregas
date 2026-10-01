"""Testes do calculador de custo (usa mock do provedor de combustível)."""

import pytest


def test_placeholder(combustivel_falso):

    pytest.skip("ainda não implementado")
import pytest

from gestao_frotas.servicos.calculador_custo import CalculadorCusto
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.veiculo import Veiculo
from gestao_frotas.excecoes import DadoInvalidoException


def criar_veiculo(consumo_medio=10.0, custo_por_km=1.5):
    return Veiculo(
        id=1,
        placa="ABC1D23",
        modelo="Fiorino",
        capacidade_de_carga=1000,
        consumo_medio=consumo_medio,
        custo_por_km=custo_por_km,
    )


def test_calcular_custo_combustivel_usando_mock(combustivel_falso):
    rota = Rota("Santa Rita", "Pouso Alegre", 300.0, 5.0)
    veiculo = criar_veiculo(consumo_medio=10.0)
    calculador = CalculadorCusto(combustivel_falso)

    custo = calculador.calcular_custo_combustivel(rota, veiculo, "MG")

    assert custo == 180.0


def test_preco_por_litro_e_chamado_com_a_uf_correta(combustivel_falso):
    rota = Rota("A", "B", 100.0, 2.0)
    veiculo = criar_veiculo()
    calculador = CalculadorCusto(combustivel_falso)

    calculador.calcular_custo_combustivel(rota, veiculo, "SP")

    combustivel_falso.preco_por_litro.assert_called_once_with("SP")


def test_litros_necessarios_sem_mock():
    rota = Rota("A", "B", 300.0, 5.0)
    veiculo = criar_veiculo(consumo_medio=12.0)
    calculador = CalculadorCusto(None)

    assert calculador.litros_necessarios(rota, veiculo) == 25.0


def test_custo_por_distancia_sem_mock():
    rota = Rota("A", "B", 300.0, 5.0)
    veiculo = criar_veiculo(custo_por_km=1.5)
    calculador = CalculadorCusto(None)

    assert calculador.custo_por_distancia(rota, veiculo) == 450.0


def test_consumo_zero_lanca_excecao():
    rota = Rota("A", "B", 300.0, 5.0)
    veiculo = criar_veiculo(consumo_medio=0)
    calculador = CalculadorCusto(None)

    with pytest.raises(DadoInvalidoException):
        calculador.litros_necessarios(rota, veiculo)