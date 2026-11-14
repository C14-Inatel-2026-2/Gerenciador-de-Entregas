import pytest
from unittest.mock import Mock

from gestao_frotas.interfaces.provedor_combustivel import ProvedorCombustivel
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.modelos.motorista import Motorista
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.veiculo import Veiculo


@pytest.fixture
def combustivel_falso():
    provedor = Mock(spec=ProvedorCombustivel)
    provedor.preco_por_litro.return_value = 6.00
    return provedor


@pytest.fixture
def motorista_falso():
    motorista = Mock(spec=Motorista)
    motorista.status = "disponível"
    return motorista

@pytest.fixture
def rota_falsa():
    rota = Mock(spec=Rota)
    rota.tempo_estimado_horas = 0.5
    return rota

@pytest.fixture
def veiculo_falso():
    veiculo = Mock(spec=Veiculo)
    veiculo.capacidade_de_carga = 10
    return veiculo

@pytest.fixture
def entregas_falsa():
    entrega1 = Mock(spec=Entrega)
    entrega2 = Mock(spec=Entrega)
    entrega1.peso = 1
    entrega2.peso = 2

    entregas = [entrega1, entrega2]
    return entregas