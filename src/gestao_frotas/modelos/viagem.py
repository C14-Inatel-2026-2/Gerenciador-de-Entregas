from enum import Enum
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.veiculo import Veiculo


class StatusViagem(Enum):
    PENDENTE = 1
    EM_ANDAMENTO = 2
    CONCLUIDO = 3

class Viagem:
    # Atributos
    __motorista: Motorista
    __veiculo: Veiculo
    __rota: Rota
    __entregas: list
    __horario_inicio: str
    __horario_termino: str
    __status: StatusViagem

    # Construtor

    def __init__(
        self, motorista: Motorista, veiculo: Veiculo, rota: Rota, entregas: list[Entrega] ,horario_inicio: str = None, horario_termino: str = None, status: StatusViagem = StatusViagem.PENDENTE):

        self.__motorista = motorista
        self.__veiculo = veiculo
        self.__rota = rota
        self.__entregas = entregas if entregas is not None else []
        self.__horario_inicio = horario_inicio
        self.__horario_termino = horario_termino
        self.__status = status

    # Métodos

    def atualizar_status(self, status: StatusViagem):
        self.__status = status

    def get_status(self):
        return self.__status


    def __repr__(self) -> str:
        return (
            f"Viagem(motorista={self.motorista}, "
            f"veiculo={self.veiculo}, "
            f"rota={self.rota}, "
            f"entregas={len(self.entregas)}, "
            f"status='{self.status}')"
        )

    @property
    def motorista(self) -> Motorista:
        return self.__motorista

    @property
    def veiculo(self) -> Veiculo:
        return self.__veiculo

    @property
    def rota(self) -> Rota:
        return self.__rota

    @property
    def entregas(self) -> list[Entrega]:
        return self.__entregas

    @property
    def horario_inicio(self):
        return self.__horario_inicio

    @property
    def horario_termino(self):
        return self.__horario_termino

