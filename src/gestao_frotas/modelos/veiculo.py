class Veiculo:
    def __init__(
        self,
        id,
        placa,
        modelo,
        capacidade_de_carga,
        consumo_medio,
        custo_por_km
    ):
        self.__id = id
        self.__placa = placa
        self.__modelo = modelo
        self.__capacidade_de_carga = capacidade_de_carga
        self.__consumo_medio = consumo_medio
        self.__custo_por_km = custo_por_km

    @property
    def id(self):
        return self.__id

    @property
    def placa(self):
        return self.__placa

    @property
    def modelo(self):
        return self.__modelo

    @property
    def capacidade_de_carga(self):
        return self.__capacidade_de_carga

    @property
    def consumo_medio(self):
        return self.__consumo_medio

    @property
    def custo_por_km(self):
        return self.__custo_por_km

    def pode_transportar(self, peso) -> bool:
        """Indica se o veículo comporta o peso informado (em kg)."""
        return peso <= self.__capacidade_de_carga
