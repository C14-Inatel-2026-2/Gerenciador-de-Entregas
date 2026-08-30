Modelo de viagem: motorista + veículo + rota, com ciclo de vida.


class StatusViagem:
    PLANEJADA = "planejada"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class Viagem:
    # TODO: iniciar(), concluir(), cancelar()
    # TODO: levantar TransicaoInvalida em mudança de status não permitida
    pass
