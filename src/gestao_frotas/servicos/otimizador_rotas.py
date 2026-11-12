from gestao_frotas.excecoes import DadoInvalidoException
from gestao_frotas.modelos.rota import Rota
from gestao_frotas.modelos.entrega import Entrega
from gestao_frotas.interfaces.provedor_mapas import ProvedorMapas


class OtimizadorRotas:

    def __init__(self, provedor_mapas: ProvedorMapas):
        self.provedor_mapas = provedor_mapas
