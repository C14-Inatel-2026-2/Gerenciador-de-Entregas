from gestao_frotas.excecoes import DadoInvalidoException, StatusInvalidoException
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.veiculo import Veiculo


class Viagem:

    # Atributos

    motorista: Motorista
    veiculo: Veiculo
    rota: Rota
    entregas: list
    horario_inicio: str
    horario_termino: str
    status: str  #(Pendente, A Caminho, Entregue?

    # Construtor

    def __init__(
        self,motorista: Motorista, veiculo: Veiculo, rota: Rota, entregas: list[Entrega] ,horario_inicio: str = None, horario_termino: str = None, status: str = "Pendente"):

        status_validos = ["Pendente", "Em Andamento", "Concluida"]
        if status not in status_validos:
            raise StatusInvalidoException(
                f"Status inicial inválido: {status}. Use: {status_validos}"
            )

        self.__motorista = motorista
        self.__veiculo = veiculo
        self.__rota = rota
        self.__entregas = entregas if entregas is not None else []
        self.__horario_inicio = horario_inicio
        self.__horario_termino = horario_termino
        self.__status = status

    # Métodos

    def atualizar_status(self, novo_status: str) -> None:
        status_validos = ["Pendente", "Em Andamento", "Concluida"]
        if novo_status not in status_validos:
            raise StatusInvalidoException(
                f"Status inválido: {novo_status}. Permitidos: {status_validos}"
            )
        self.__status = novo_status

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

    @property
    def status(self) -> str:
        return self.__status