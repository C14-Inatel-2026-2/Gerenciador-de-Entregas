# Gerenciador de Entregas

Gerenciador de frotas e rotas de entrega.

## Funcionalidades

- Gestão de motoristas e veículos
- Criação de rotas otimizadas
- Cálculo de custo da rota
- Gerenciamento de viagem

## Stack

Python 3.11+, pytest, pytest-mock.

## Como rodar

Na raiz do projeto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Rodar os testes:

```powershell
pytest
pytest --cov=gestao_frotas    # com cobertura
```

## Estrutura

- `src/gestao_frotas/modelos` — entidades do domínio
- `src/gestao_frotas/interfaces` — contratos (Protocol) do que vem de fora
- `src/gestao_frotas/servicos` — regras de negócio
- `src/gestao_frotas/repositorios` — persistência
- `tests/unitarios` — testes isolados, com mock nas interfaces
- `tests/integracao` — fluxos de ponta a ponta

Os serviços recebem as dependências externas por injeção, via as interfaces.
Assim os testes substituem elas por mock e nenhum teste unitário faz chamada de rede.
