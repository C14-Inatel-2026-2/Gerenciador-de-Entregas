from gestao_frotas.excecoes import StatusInvalidoException


class Motorista:
    STATUS_DISPONIVEL = "disponível"
    STATUS_EM_VIAGEM = "em viagem"
    STATUS_INDISPONIVEL = "indisponível"

    STATUS_VALIDOS = {
        STATUS_DISPONIVEL,
        STATUS_EM_VIAGEM,
        STATUS_INDISPONIVEL,
    }

    def __init__(self, id: int, nome: str, cnh, status=STATUS_DISPONIVEL):
        if status not in self.STATUS_VALIDOS:
            raise ValueError("Status de motorista inválido.")

        self.__id = id
        self.__nome = nome
        self.__cnh = cnh
        self.__status = status

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def cnh(self):
        return self.__cnh

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        if valor not in self.STATUS_VALIDOS:
            raise StatusInvalidoException("Status de motorista inválido.")
        self.__status = valor