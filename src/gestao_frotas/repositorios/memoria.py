"""Repositório em memória, suficiente para o escopo do projeto."""


class RepositorioEmMemoria:
    def __init__(self) -> None:
        self._itens: dict = {}

    # TODO: salvar(), buscar_por_id(), listar()
