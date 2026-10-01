"""Testes unitários do modelo Rota."""

import pytest

from gestao_frotas.modelos.rota import Rota
from gestao_frotas.excecoes import DadoInvalidoException


def test_criar_rota_valida_guarda_os_atributos():
    rota = Rota(1, "Santa Rita", "Itajuba", 60.0, 1.5)

    assert rota.id == 1
    assert rota.origem == "Santa Rita"
    assert rota.destino == "Itajuba"
    assert rota.distancia_km == 60.0
    assert rota.tempo_estimado_horas == 1.5


@pytest.mark.parametrize("distancia_invalida", [0, -5])
def test_distancia_menor_ou_igual_a_zero_lanca_excecao(distancia_invalida):
    with pytest.raises(DadoInvalidoException):
        Rota(1, "A", "B", distancia_invalida, 2)


@pytest.mark.parametrize("tempo_invalido", [0, -1])
def test_tempo_estimado_menor_ou_igual_a_zero_lanca_excecao(tempo_invalido):
    with pytest.raises(DadoInvalidoException):
        Rota(1, "A", "B", 100, tempo_invalido)


def test_velocidade_media_kmh_calcula_corretamente():
    rota = Rota(1, "A", "B", 120.0, 2.0)

    assert rota.velocidade_media_kmh() == 60.0


def test_repr_inclui_o_id_e_nao_quebra():
    rota = Rota(7, "A", "B", 10, 1)

    texto = repr(rota)

    assert "id=7" in texto
