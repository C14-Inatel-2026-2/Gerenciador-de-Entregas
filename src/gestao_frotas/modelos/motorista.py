class Motorista:
    STATUS_DISPONIVEL = "disponível"
    STATUS_EM_VIAGEM = "em viagem"
    STATUS_INDISPONIVEL = "indisponível"

    STATUS_VALIDOS = {
        STATUS_DISPONIVEL,
        STATUS_EM_VIAGEM,
        STATUS_INDISPONIVEL,
    }

    TIPOS_VEICULO_VALIDOS = {"carro", "caminhão"}

    def __init__(self, id, nome, cnh, status=STATUS_DISPONIVEL):
        if status not in self.STATUS_VALIDOS:
            raise ValueError("Status de motorista inválido.")

        self.id = id
        self.nome = nome
        self.cnh = cnh
        self.status = status

    def atualizar_status(self, novo_status):
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError("Status de motorista inválido.")

        self.status = novo_status

    def atribuir_veiculo(self, veiculo):
        tipos_permitidos = self.cnh.get(next(iter(self.cnh)), [])

        if veiculo.tipo not in tipos_permitidos:
            raise ValueError("Motorista não pode dirigir este veículo.")

        self.veiculo = veiculo