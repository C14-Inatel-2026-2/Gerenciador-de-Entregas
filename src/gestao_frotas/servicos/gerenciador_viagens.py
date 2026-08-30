"""Orquestra o ciclo de vida das viagens.

Aloca motorista e veículo, valida disponibilidade e controla o status.
"""


class GerenciadorViagens:
    def __init__(self, repositorio) -> None:
        self._repo = repositorio

    # TODO: criar_viagem(), iniciar(), concluir(), cancelar()
