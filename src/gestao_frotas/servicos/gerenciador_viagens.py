from gestao_frotas.excecoes import CapacidadeExcedidaException, DadoInvalidoException
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.modelos.veiculo import Veiculo
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.viagem import Viagem,StatusViagem
from datetime import datetime, timedelta
from gestao_frotas.servicos.calculador_custo import CalculadorCusto


class GerenciadorViagens:

    def __init__(self):
        self.__viagens_em_andamento: list[Viagem] = []

    def iniciar_viagem(self, motorista: Motorista, veiculo: Veiculo, entregas: list[Entrega]):
        horario_inicio = datetime.now()

        peso_total = sum(entrega.peso for entrega in entregas)

        if peso_total > veiculo.capacidade_de_carga:
            raise CapacidadeExcedidaException (
                f'A peso é superior a capacidade de carga do veículo.'
            )

        if motorista.status != Motorista.STATUS_DISPONIVEL:
            raise DadoInvalidoException (
                f'O motorista {motorista.nome} não está disponível para entrega.'
            )

        viagem = Viagem(motorista, veiculo, entregas, horario_inicio)

        self.__viagens_em_andamento.append(viagem)
        viagem.atualizar_status(StatusViagem.EM_ANDAMENTO)
        motorista.atualizar_status("em viagem")

    def finalizar_viagem(self, viagem: Viagem):
        viagem.atualizar_status(StatusViagem.CONCLUIDO)
        viagem.motorista.atualizar_status("disponível")
        self.__viagens_em_andamento.remove(viagem)

    def listar_viagems(self):
        for viagem in self.__viagens_em_andamento:
            viagem.__repr__()

    @property
    def viagems(self):
        return self.__viagens_em_andamento