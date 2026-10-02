"""Testes unitários de rota."""
import pytest
from gestao_frotas.modelos.rota import Rota


class TestRota:
    @pytest.fixture
    def rota(self) -> Rota:
        return Rota("Santa Rita", "Pouso Alegre", 20, 0.5)


    def test_construtor(self, rota: Rota):
        assert rota.destino == "Pouso Alegre"
        assert rota.origem == "Santa Rita"
        assert rota.distancia_km == 20
        assert rota.tempo_estimado_horas == 0.5





