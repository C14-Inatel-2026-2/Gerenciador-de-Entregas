from enum import Enum
from gestao_frotas.excecoes import DadoInvalidoException



class StatusEntrega(Enum):
    PENDENTE = 1
    A_CAMINHO = 2
    ENTREGA = 3

class Prioridade(Enum):
    BAIXA = 1
    NORMAL = 2
    ALTA = 3

class Entrega:

    # atributos
    __id : int
    __endereco_origem : str
    __endereco_destino : str
    __peso : float
    __prioridade : Prioridade
    __status : StatusEntrega

    #Construtor
    def __init__(self, id:int, endereco_origem:str, endereco_destino: str, peso:float, prioridade: Prioridade = Prioridade.NORMAL, status: StatusEntrega = StatusEntrega.PENDENTE) -> None:
        if peso<=0:
            raise DadoInvalidoException("O Peso tem que ser maior que zero.")

        self.__id = id
        self.__endereco_origem = endereco_origem
        self.__endereco_destino = endereco_destino
        self.__peso = peso
        self.__prioridade = prioridade
        self.__status = status

    # métodos

    def atualizar_status(self, status: StatusEntrega) -> None:
        self.__status = status

    def atualizar_prioridade(self, prioridade: Prioridade) -> None:
        self.__prioridade = prioridade


    def __repr__(self) -> str:
        return (
            f"Entrega(id={self.__id}, "
            f"origem='{self.__endereco_origem}', "
            f"destino='{self.__endereco_destino}', "
            f"peso={self.__peso}kg, "
            f"prioridade='{self.__prioridade}', "
            f"status='{self.__status}')"
        )

    @property
    def id(self) -> int:
        return self.__id

    @property
    def origem(self) -> str:
        return self.__endereco_origem

    @property
    def destino(self) -> str:
        return self.__endereco_destino

    @property
    def peso(self) -> float:
        return self.__peso

    @property
    def prioridade(self) -> str:
        return self.__prioridade

    # TODO: VERIFICAR COM WILLIAM, A NECESSIDADE DE TER ESSE PROPERTY, DADO QUE JÁ TEMOS UM MÉTODO QUE ATUALIZA O STATUS
    @property
    def status(self) -> str:
        return self.__status