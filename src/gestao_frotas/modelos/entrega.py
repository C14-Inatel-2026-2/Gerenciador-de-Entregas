
from gestao_frotas.excecoes import DadoInvalidoException, StatusInvalidoException


class Entrega:


    # atributos
    id : int
    endereco_origem : str
    endreco_destino : str
    peso : float
    prioridade : str #(Baixa, Normal, Alta)?
    status : str #(Pendente, A Caminho, Entregue?

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


        self.id = id
        self.endereco_origem = endereco_origem
        self.endereco_destino = endereco_destino
        self.peso = peso
        self.prioridade = prioridade
        self.status = status

    # métodos

    # alterar prioridade

    def alterar_prioridade(self, nova_prioridade: str) -> None:
        prioridades_validas = ["Baixa", "Normal", "Alta"]
        if nova_prioridade not in prioridades_validas:
            raise DadoInvalidoException(
                f"Prioridade inválida: {nova_prioridade}. Use: {prioridades_validas}"
            )
        self.prioridade = nova_prioridade

    #alterar status

    def atualizar_status(self, novo_status: str) -> None:
        status_validos = ["Pendente", "A Caminho", "Entregue"]
        if novo_status not in status_validos:
            raise StatusInvalidoException(
                f"Status inválido: {novo_status}. Permitidos: {status_validos}"
            )
        self.status = novo_status

    def __repr__(self) -> str:
        return (
            f"Entrega(id={self.id}, "
            f"origem='{self.endereco_origem}', "
            f"destino='{self.endereco_destino}', "
            f"peso={self.peso}kg, "
            f"prioridade='{self.prioridade}', "
            f"status='{self.status}')"
        )