
from gestao_frotas.excecoes import DadoInvalidoException, StatusInvalidoException


class Entrega:

    # atributos
    __id : int
    __endereco_origem : str
    __endreco_destino : str
    __peso : float
    __prioridade : str #(Baixa, Normal, Alta)?
    __status : str #(Pendente, A Caminho, Entregue?

    #Construtor
    def __init__(self, id:int, endereco_origem:str, endereco_destino: str, peso:float, prioridade: str = "Normal", status:str = "Pendente"):
        if peso<=0:
            raise DadoInvalidoException("O Peso tem que ser maior que zero.")

        prioridades_validas = ["Baixa", "Normal", "Alta"]
        if prioridade not in prioridades_validas:
            raise DadoInvalidoException(
                f"Prioridade inválida: {prioridade}. Use: {prioridades_validas}"
            )

        status_validos = ["Pendente", "A Caminho", "Entregue"]
        if status not in status_validos:
            raise StatusInvalidoException(
                f"Status inicial inválido: {status}. Use: {status_validos}"
            )


        self.__id = id
        self.__endereco_origem = endereco_origem
        self.__endereco_destino = endereco_destino
        self.__peso = peso
        self.__prioridade = prioridade
        self.__status = status

    # métodos

    # alterar prioridade

    def alterar_prioridade(self, nova_prioridade: str) -> None:
        prioridades_validas = ["Baixa", "Normal", "Alta"]
        if nova_prioridade not in prioridades_validas:
            raise DadoInvalidoException(
                f"Prioridade inválida: {nova_prioridade}. Use: {prioridades_validas}"
            )
        self.__prioridade = nova_prioridade

    #alterar status

    def atualizar_status(self, novo_status: str) -> None:
        status_validos = ["Pendente", "A Caminho", "Entregue"]
        if novo_status not in status_validos:
            raise StatusInvalidoException(
                f"Status inválido: {novo_status}. Permitidos: {status_validos}"
            )
        self.__status = novo_status

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

    @property
    def status(self) -> str:
        return self.__status