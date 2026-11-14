"""Testes unitários de entrega."""

import pytest

from gestao_frotas.modelos.entrega import Entrega,Prioridade,StatusEntrega


class TestEntrega:
    @pytest.fixture
    def entrega(self) -> Entrega:
        return Entrega(0, "Pouso Alegre", "Santa Rita",10.5,Prioridade.NORMAL, StatusEntrega.PENDENTE )

    def test_atualizar_status(self, entrega):
        entrega.atualizar_status(StatusEntrega.PENDENTE)
        assert entrega.get_status() == StatusEntrega.PENDENTE

        entrega.atualizar_status(StatusEntrega.A_CAMINHO)
        assert entrega.get_status() == StatusEntrega.A_CAMINHO

        entrega.atualizar_status(StatusEntrega.ENTREGUE)
        assert entrega.get_status() == StatusEntrega.ENTREGUE

    def test_atualizar_prioridade(self, entrega):
        entrega.atualizar_prioridade(Prioridade.NORMAL)
        assert entrega.get_prioridade() == Prioridade.NORMAL

        entrega.atualizar_prioridade(Prioridade.BAIXA)
        assert entrega.get_prioridade() == Prioridade.BAIXA

        entrega.atualizar_prioridade(Prioridade.ALTA)
        assert entrega.get_prioridade() == Prioridade.ALTA