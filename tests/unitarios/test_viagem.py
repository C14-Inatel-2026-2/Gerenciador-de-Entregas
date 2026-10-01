"""Testes unitários de viagem."""

import pytest

from gestao_frotas.modelos.entrega import Entrega, StatusEntrega, Prioridade
from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.veiculo import Veiculo
from gestao_frotas.modelos.viagem import Viagem, StatusViagem

class TestViagem:
    @pytest.fixture
    def viagem(self) -> Viagem:
       motorista: Motorista = Motorista(0,"Victor","A")
       veiculo: Veiculo = Veiculo(0,"abc1234","Carreta", 100, 50,10)
       rota: Rota = Rota("Santa Rita", "Pouso Alegre", 20, 0.5)
       entregas: list[Entrega] = [Entrega(0, "Pouso Alegre", "Santa Rita",10.5,Prioridade.NORMAL, StatusEntrega.PENDENTE ),
                                  Entrega(1, "Pouso Alegre", "Santa Rita",20,Prioridade.ALTA, StatusEntrega.PENDENTE )    ]
       horario_inicio: str = None
       horario_termino: str = None
       status: StatusViagem = StatusViagem.PENDENTE
       return Viagem(motorista, veiculo, rota, entregas, horario_inicio, horario_termino, status)


    def test_atualizar_status(self, viagem: Viagem):
        viagem.atualizar_status(StatusViagem.PENDENTE)
        assert viagem.get_status() == StatusViagem.PENDENTE

        viagem.atualizar_status(StatusViagem.EM_ANDAMENTO)
        assert viagem.get_status() == StatusViagem.EM_ANDAMENTO

        viagem.atualizar_status(StatusViagem.CONCLUIDO)
        assert viagem.get_status() == StatusViagem.CONCLUIDO


