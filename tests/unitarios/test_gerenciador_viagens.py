import pytest

from gestao_frotas.excecoes import DadoInvalidoException, CapacidadeExcedidaException
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.veiculo import Veiculo
from gestao_frotas.servicos.gerenciador_viagens import GerenciadorViagens
from freezegun import freeze_time
from datetime import datetime

def criar_viagem():
    cnh = {"123": ["caminhão"]}
    motorista = Motorista(0, 'will', cnh)
    rota = Rota("Santa Rita", "Pouso Alegre", 28, 0.5)
    veiculo = Veiculo(0, "abc1234", "X", 120, 45, 11, "carro")
    entrega1 = Entrega(0, "Santa Rita", "Pouso Alegre", 12)
    entrega2 = Entrega(1, "Santa Rita", "Pouso Alegre", 11)
    entregas = [entrega1, entrega2]

    return motorista, rota, veiculo, entregas

def test_atribuicao_motorista_invalido():
    motorista, rota, veiculo, entrega = criar_viagem()
    gerenciador = GerenciadorViagens()

    motorista.atualizar_status("indisponível")

    with pytest.raises(DadoInvalidoException):
        gerenciador.iniciar_viagem(motorista, rota, veiculo, entrega)

@freeze_time("2021-07-30 12:00:00")
def test_horario_inicial():
    motorista, rota, veiculo, entregas = criar_viagem()
    gerenciador = GerenciadorViagens()
    gerenciador.iniciar_viagem(motorista, rota, veiculo, entregas)

    with freeze_time("2021-07-30 12:00:00"):
        agora = datetime.now()
        assert gerenciador.viagems[0].horario_inicio == agora

@freeze_time("2021-07-30 12:00:00")
def test_horario_termino():
    motorista, rota, veiculo, entregas = criar_viagem()
    gerenciador = GerenciadorViagens()
    gerenciador.iniciar_viagem(motorista, rota, veiculo, entregas)

    with freeze_time("2021-07-30 12:00:00"):
        horario = datetime(2021, 7, 30, 12, 30, 0)
        assert gerenciador.viagems[0].horario_termino == horario

def test_finalizar_viagem_com_mock(motorista_falso, rota_falsa, veiculo_falso, entregas_falsa):
    gerenciador = GerenciadorViagens()
    gerenciador.iniciar_viagem(motorista_falso, rota_falsa, veiculo_falso, entregas_falsa)

    gerenciador.finalizar_viagem(gerenciador.viagems[0])
    assert gerenciador.viagems == []

def test_capacidade_excedida_com_mock(motorista_falso, rota_falsa, veiculo_falso):
    gerenciador = GerenciadorViagens()
    entrega1 = Entrega(0, "Santa Rita", "Pouso Alegre", 12)
    entrega2 = Entrega(1, "Santa Rita", "Pouso Alegre", 11)
    entregas = [entrega1, entrega2]
    with pytest.raises(CapacidadeExcedidaException):
        gerenciador.iniciar_viagem(motorista_falso, rota_falsa, veiculo_falso, entregas)