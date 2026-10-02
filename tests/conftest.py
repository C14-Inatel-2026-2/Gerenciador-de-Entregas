import pytest
from unittest.mock import Mock

from gestao_frotas.interfaces.provedor_combustivel import ProvedorCombustivel


@pytest.fixture
def combustivel_falso():
    provedor = Mock(spec=ProvedorCombustivel)
    provedor.preco_por_litro.return_value = 6.00
    return provedor
