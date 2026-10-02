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

    def test_atualizar_status_invalido_deve_lancar_excecao(self, viagem: Viagem):
        status_invalido = "STATUS_INVENTADO"
        with pytest.raises(ValueError, match="Status inválido"):
            viagem.atualizar_status(status_invalido)


def test_inicializacao_viagem(mocker):
    # Criamos objetos vazios para simular as dependências
    mock_motorista = mocker.Mock()
    mock_veiculo = mocker.Mock()
    mock_rota = mocker.Mock()
    mock_entrega_1 = mocker.Mock()
    mock_entrega_2 = mocker.Mock()

    viagem = Viagem(
        motorista=mock_motorista,
        veiculo=mock_veiculo,
        rota=mock_rota,
        entregas=[mock_entrega_1, mock_entrega_2]
    )

    assert viagem.motorista == mock_motorista
    assert viagem.veiculo == mock_veiculo
    assert viagem.rota == mock_rota
    assert len(viagem.entregas) == 2
    assert viagem.get_status() == StatusViagem.PENDENTE
    assert viagem.horario_inicio is None


def test_representacao_viagem_com_mocks(mocker):
    mock_motorista = mocker.Mock()
    mock_motorista.__str__ = mocker.Mock(return_value="MotoristaMock")

    mock_veiculo = mocker.Mock()
    mock_veiculo.__str__ = mocker.Mock(return_value="VeiculoMock")

    mock_rota = mocker.Mock()
    mock_rota.__str__ = mocker.Mock(return_value="RotaMock")

    mock_entregas = [mocker.Mock(), mocker.Mock(), mocker.Mock()]

    viagem = Viagem(
        motorista=mock_motorista,
        veiculo=mock_veiculo,
        rota=mock_rota,
        entregas=mock_entregas,
        status=StatusViagem.EM_ANDAMENTO
    )

    resultado_repr = repr(viagem)

    assert "entregas=3" in resultado_repr
    assert "StatusViagem.EM_ANDAMENTO" in resultado_repr