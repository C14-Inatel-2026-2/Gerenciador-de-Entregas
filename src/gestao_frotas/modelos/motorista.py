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
        self._validar_status(status)

        self.id = id
        self.nome = nome
        self.cnh = cnh
        self.status = status

    def _validar_status(self, status):
        if status not in self.STATUS_VALIDOS:
            raise ValueError("Status de motorista inválido.")

    def atualizar_status(self, novo_status):
        self._validar_status(novo_status)
        self.status = novo_status

    def _validar_veiculo(self, veiculo):
        tipos_permitidos = self.cnh.get(next(iter(self.cnh)), [])

        if veiculo.tipo not in tipos_permitidos:
            raise ValueError("Motorista não pode dirigir este veículo.")

    def atribuir_veiculo(self, veiculo):
        self._validar_veiculo(veiculo)
        self.veiculo = veiculo
