"""Testes unitários de rota."""
import pytest
from gestao_frotas.modelos.rota import Rota
from freezegun import freeze_time
from datetime import datetime, timedelta

class TestRota:
    @pytest.fixture
    def rota(self) -> Rota:
        return Rota("Santa Rita", "Pouso Alegre", 20)


    def test_construtor(self, rota: Rota):
        assert rota.destino == "Pouso Alegre"
        assert rota.origem == "Santa Rita"
        assert rota.distancia_km == 20

    @freeze_time("2021-07-30 12:00:00")
    def test_horario_termino(self):
        rota = Rota("Santa Rita", "Pouso Alegre", 20)

        with (freeze_time("2021-07-30 12:00:00")):
            horario = datetime(2021, 7, 30, 12, 15, 0)
            tempo_delta = timedelta(hours=rota.tempo_estimado_horas)

            assert (datetime.now() + tempo_delta) == horario




