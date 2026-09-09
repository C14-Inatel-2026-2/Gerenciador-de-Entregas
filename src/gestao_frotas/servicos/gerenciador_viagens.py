from gestao_frotas.excecoes import CapacidadeExcedidaException, StatusInvalidoException
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.modelos.veiculo import Veiculo
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.viagem import Viagem
from datetime import datetime

class GerenciadorViagens:

    def __init__(self):
        self.__viagens_em_andamento: list[Viagem] = []

    def iniciar_viagem(self, motorista: Motorista, rota: Rota, veiculo: Veiculo, entregas: list[Entrega]):
        horario_inicio = datetime.now()
        horario_termino = None

        peso_total = sum(entrega.peso for entrega in entregas)

        if peso_total > veiculo.capacidade_de_carga:
            raise CapacidadeExcedidaException (
                f'A peso é superior a capacidade de carga do veículo.'
            )

        if motorista.status != Motorista.STATUS_DISPONIVEL:
            raise StatusInvalidoException (
                f'O motorista {motorista.nome} não está disponível para entrega.'
            )

        viagem = Viagem(motorista, veiculo, rota, entregas, horario_inicio, horario_termino)
        self.__viagens_em_andamento.append(viagem)
        viagem.atualizar_status("Em Andamento")
        #motorista.setStatus("em viagem")

    def finalizar_viagem(self, viagem: Viagem):
        viagem.atualizar_status("Concluída")
        viagem.motorista.status = Motorista.STATUS_DISPONIVEL
        self.__viagens_em_andamento.remove(viagem)

    def listar_viagems(self):
        for viagem in self.__viagens_em_andamento:
            viagem.__repr__()





