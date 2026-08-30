"""Exceções do domínio."""


class ErroDeDominio(Exception):
    """Base para todos os erros de regra de negócio do projeto."""


class MotoristaIndisponivel(ErroDeDominio):
    pass


class VeiculoIndisponivel(ErroDeDominio):
    pass


class CapacidadeExcedida(ErroDeDominio):
    pass


class TransicaoInvalida(ErroDeDominio):
    """Mudança de status de viagem que não é permitida."""
