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

    def iniciar_viagem(self, motorista: Motorista, rota: Rota, veiculo: Veiculo, entregas: list[Entrega]):
        horario_inicio = datetime.now()
        horario_termino = horario_inicio + timedelta(hours=rota.tempo_estimado_horas)

        peso_total = sum(entrega.peso for entrega in entregas)

        if peso_total > veiculo.capacidade_de_carga:
            raise CapacidadeExcedidaException (
                f'A peso é superior a capacidade de carga do veículo.'
            )

        if motorista.status != Motorista.STATUS_DISPONIVEL:
            raise DadoInvalidoException (
                f'O motorista {motorista.nome} não está disponível para entrega.'
            )

        '''
        try:
            motorista.atribuir_veiculo(veiculo)
        except ValueError:
            raise DadoInvalidoException (
                f'O veículo não pode ser atribuído a esse motorista.'
            )
        
        calculador = CalculadorCusto(None)
        custo_total = calculador.calcular_custo_combustivel(rota, veiculo, '')
        custo_total +=  calculador.custo_por_distancia(rota, veiculo)

        viagem.addCustoTotal(custo_total)
        '''

        viagem = Viagem(motorista, veiculo, rota, entregas, horario_inicio, horario_termino)

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