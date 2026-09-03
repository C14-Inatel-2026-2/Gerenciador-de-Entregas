from gestao_frotas.excecoes import DadoInvalidoException, StatusInvalidoException
from gestao_frotas.modelos.rota import Rota



class Viagem:

    # Atributos

    motorista: "Motorista" #Aguardando Classe Gabriel
    veiculo: "Veiculo" #Aguardando Classe Gabriel
    rota: Rota
    entregas: list
    horario_inicio: str
    horario_termino: str
    status: str  #(Pendente, A Caminho, Entregue?

    # Construtor

    def __init__(
        self,motorista: object, veiculo: object,rota: object, entregas: list = None,horario_inicio: str = None, horario_termino: str = None, status: str = "Pendente"):

        status_validos = ["Pendente", "Em Andamento", "Concluida"]
        if status not in status_validos:
            raise StatusInvalidoException(
                f"Status inicial inválido: {status}. Use: {status_validos}"
            )

        self.motorista = motorista
        self.veiculo = veiculo
        self.rota = rota
        self.entregas = entregas if entregas is not None else []
        self.horario_inicio = horario_inicio
        self.horario_termino = horario_termino
        self.status = status

    # Métodos

    def atualizar_status(self, novo_status: str) -> None:
        status_validos = ["Pendente", "Em Andamento", "Concluida"]
        if novo_status not in status_validos:
            raise StatusInvalidoException(
                f"Status inválido: {novo_status}. Permitidos: {status_validos}"
            )
        self.status = novo_status

    def __repr__(self) -> str:
        return (
            f"Viagem(motorista={self.motorista}, "
            f"veiculo={self.veiculo}, "
            f"rota={self.rota}, "
            f"entregas={len(self.entregas)}, "
            f"status='{self.status}')"
        )
