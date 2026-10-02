from gestao_frotas.excecoes import DadoInvalidoException


class Rota:

    # Atributos
    __id: int
    __origem: str
    __destino: str
    __distancia_km: float
    __tempo_estimado_horas: float

   #Construtor

    def __init__(self, origem: str, destino: str, distancia_km: float, tempo_estimado_horas: float ):
        if distancia_km <= 0:
            raise DadoInvalidoException("A distância deve ser maior que zero.")

        if tempo_estimado_horas <= 0:
            raise DadoInvalidoException("O tempo estimado deve ser maior que zero.")

        self.__origem = origem
        self.__destino = destino
        self.__distancia_km = distancia_km
        self.__tempo_estimado_horas = tempo_estimado_horas


    # Métodos
    def __repr__(self) -> str:
        return (
            f"Rota(id={self.__id}, "
            f"origem='{self.__origem}', "
            f"destino='{self.__destino}', "
            f"distancia={self.__distancia_km}km, "
            f"tempo={self.__tempo_estimado_horas}h)"
        )

    @property
    def origem(self) -> str:
        return self.__origem

    @property
    def destino(self) -> str:
        return self.__destino

    @property
    def distancia_km(self) -> float:
        return self.__distancia_km

    @property
    def tempo_estimado_horas(self) -> float:
        return self.__tempo_estimado_horas
