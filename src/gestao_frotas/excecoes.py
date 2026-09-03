
class GestaoFrotasException(Exception):
    """Exceção base para todas as regras de negócio do sistema de frotas."""
    pass


class DadoInvalidoException(GestaoFrotasException):
    """Lançada quando algum campo ou valor numérico for inválido (ex: peso <= 0, prioridade desconhecida)."""
    pass


class StatusInvalidoException(GestaoFrotasException):
    """Lançada quando um status fora do fluxo permitido for informado."""
    pass


class CapacidadeExcedidaException(GestaoFrotasException):
    """Lançada quando o peso total das entregas ultrapassar o limite do veículo."""
    pass