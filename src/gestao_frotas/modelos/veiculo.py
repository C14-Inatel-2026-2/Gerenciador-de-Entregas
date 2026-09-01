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
        self.id = id
        self.placa = placa
        self.modelo = modelo
        self.capacidade_de_carga = capacidade_de_carga
        self.consumo_medio = consumo_medio
        self.custo_por_km = custo_por_km
