class Motorista:
    STATUS_DISPONIVEL = "disponível"
    STATUS_EM_VIAGEM = "em viagem"
    STATUS_INDISPONIVEL = "indisponível"

    STATUS_VALIDOS = {
        STATUS_DISPONIVEL,
        STATUS_EM_VIAGEM,
        STATUS_INDISPONIVEL,
    }

    def __init__(self, id, nome, cnh, status=STATUS_DISPONIVEL):
        if status not in self.STATUS_VALIDOS:
            raise ValueError("Status de motorista inválido.")

        self.id = id
        self.nome = nome
        self.cnh = cnh
        self.status = status
