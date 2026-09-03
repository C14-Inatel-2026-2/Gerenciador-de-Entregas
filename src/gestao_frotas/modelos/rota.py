from gestao_frotas.excecoes import DadoInvalidoException


class Rota:

    # Atributos

    id: int
    origem: str
    destino: str
    distancia_km: float
    tempo_estimado_horas: float

   #Construtor

    def __init__(self,id: int, origem: str, destino: str, distancia_km: float, tempo_estimado_horas: float ):
        if distancia_km <= 0:
            raise DadoInvalidoException("A distância deve ser maior que zero.")

        if tempo_estimado_horas <= 0:
            raise DadoInvalidoException("O tempo estimado deve ser maior que zero.")

        self.id = id
        self.origem = origem
        self.destino = destino
        self.distancia_km = distancia_km
        self.tempo_estimado_horas = tempo_estimado_horas


    # Métodos






    def __repr__(self) -> str:
        return (
            f"Rota(id={self.id}, "
            f"origem='{self.origem}', "
            f"destino='{self.destino}', "
            f"distancia={self.distancia_km}km, "
            f"tempo={self.tempo_estimado_horas}h)"
        )
