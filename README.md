## 1) Descrição do Projeto
O Gerenciador de Entregas é um sistema desenvolvido em Python com o objetivo de facilitar a organização e o controle das entregas.

A ideia do projeto é reunir em um só lugar as informações dos motoristas, veículos e entregas, facilitando o acompanhamento dos cadastros, a disponibilidade dos motoristas e a situação de cada entrega.

Além disso, o sistema busca ajudar no planejamento das rotas, considerando fatores como a distância, a capacidade de carga dos veículos e os custos de transporte. Dessa forma, o projeto tem como objetivo tornar o gerenciamento das entregas mais simples, organizado e eficiente.

## 2) O Users Storys no Jira
As User Stories do projeto foram estruturadas individualmente como cards no Jira. 
Ao abrir qualquer item do quadro, a seção de detalhes apresenta a descrição completa da funcionalidade, acompanhada de seus respectivos requisitos e critérios de aceitação. 

O acompanhamento pode ser feito pelo link: https://s03-gerenciador.atlassian.net/jira/software/projects/SCRUM/pages.

## 3) Uso de Inteligência Artificial no Projeto

### Uso de IA (Gemini) — Job de Lint no Jenkinsfile (Willian)
Estes são os registros do uso do Google Gemini para a configuração da etapa de análise estática de código (Lint) no pipeline:
- **Ferramenta Utilizada:** Google Gemini.
- **Prompt e Dúvida Principal:** Solicitação ao Gemini de como estruturar e configurar o job (stage) de Lint dentro do `Jenkinsfile` para validação automática da qualidade e padronização do código no pipeline.
- **Código Gerado pela IA:** O Gemini forneceu a estrutura completa do estágio de Lint pronta para uso direto no pipeline do Jenkins.
- **Avaliação e Ajustes (Troubleshooting):** A resposta fornecida pelo Gemini foi totalmente satisfatória e funcional de imediato, a ponto de não precisar de nenhuma alteração ou correção posterior.

### Uso de IA (Gemini) — Job de Deploy e Integração com o Render (Diego Victor)
Estes são os prompts e arquivos gerados com auxílio do Google Gemini para a etapa de publicação contínua:
- **Ferramenta Utilizada:** Google Gemini.
- **Criação do Stage de Deploy (Jenkinsfile):** Solicitação de criação e explicação de um stage de Deploy dentro do `Jenkinsfile` condicionado à branch `main`, disparando o deploy hook do Render de forma segura com `withCredentials` e comando de terminal (`curl -fsS -X POST "$RENDER_HOOK"`).
- **Estrutura de Containers (Dockerfile):** Questionamento sobre a necessidade de múltiplos Dockerfiles (um para o Jenkins e outro para o Render) e geração do `Dockerfile` na raiz focado no ambiente de produção do Render utilizando a imagem `python:3.11-slim`, cópia dos arquivos, instalação via `pip install .` e inicialização dinâmica da porta.
- **Servidor Base da Aplicação (app.py):** Geração do código base do servidor utilizando o framework Flask, criando a rota raiz (`/`) e a instância `app` para ser consumida pelo servidor web em produção.

#### Avaliação e Ajustes (Troubleshooting) — Deploy no Render
A resposta inicial do Google Gemini não foi satisfatória, pois ocorreram vários erros durante a execução como os mostrados abaixo, sendo necessário utilizá-la novamente para corrigir os problemas:
- **Resolução do Erro 128 no Render (Falha de Inicialização):** O Gemini foi utilizado para interpretar os logs (`Exited with status 128`) e identificar que o container falhava porque o comando inicial procurava um arquivo inexistente, corrigindo a última linha do `Dockerfile` para `CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-10000}"]`.
- **Correção de Sintaxe Python (Dunder Variables):** Resolução do erro `NameError: name '_name_' is not defined` no arquivo `app.py` com o suporte do Gemini, ajustando o formato incorreto gerado com um sublinhado (`_name_`) para o padrão correto da linguagem com dois sublinhados (`__name__` e `__main__`).
- **Ajuste de Dependências de Produção (pyproject.toml):** Orientação do Gemini para transferir as bibliotecas `flask` e `gunicorn` das dependências de desenvolvimento (`dev`) para as dependências principais da aplicação no `pyproject.toml`, garantindo sua instalação durante o build no Render.

### Uso de IA — Sintaxe de Testes Unitários de Entrega e Rota (Diego Victor)
Estes são os detalhes do uso da IA como apoio para a definição e estruturação dos testes das classes `Entrega` e `Rota`:
- **Ferramenta Utilizada:** Google Gemini.
- **Prompt e Objetivo:** Solicitação de ideias de cenários de teste e consulta sobre a sintaxe correta do `pytest` (como o uso de `@pytest.fixture` e `assert`) para realizar a implementação manual dos testes unitários de atualização de status (`StatusEntrega`), prioridade (`Prioridade`) e validação de atributos do construtor nas classes `Entrega` e `Rota`.
- **Avaliação e Ajustes (Troubleshooting):** A resposta da IA foi satisfatória tanto na sugestão dos casos de teste quanto na explicação da sintaxe do framework, permitindo que ambos os arquivos de teste fossem escritos e executados sem erros ou necessidade de ajustes adicionais.

### Uso de IA — Geração de Testes Unitários com Mock para Viagem (Diego Victor)
Estes são os detalhes do uso da IA para a criação dos testes mais complexos da classe `Viagem`:
- **Ferramenta Utilizada:** Google Gemini.
- **Prompt e Objetivo:** Solicitação de geração de código de testes unitários utilizando `pytest` e `pytest-mock` (`mocker.Mock`) para a classe `Viagem`, visto que ela depende de múltiplas outras classes (`Motorista`, `Veiculo`, `Rota` e `Entrega`). O objetivo foi obter a implementação pronta de simulação de objetos (`mocks`), validação de inicialização, representação textual (`repr`) e tratamento de exceções com `pytest.raises` para status inválidos.
- **Avaliação e Ajustes (Troubleshooting):** A resposta da IA foi satisfatória, fornecendo o código estruturado com os `mocks` e as validações de exceção prontos para uso, permitindo testar a classe `Viagem` de forma isolada sem a necessidade de correções adicionais.

### Uso de IA — Outros Usos (Gabriel Perroni)
Estes são os detalhes do uso da IA para validação do código antes do envio ao repositório:
- **Ferramenta Utilizada:** Google Gemini.
- **Prompt e Objetivo:** Solicitação de revisão preventiva da lógica e da sintaxe do código desenvolvido pelo integrante (Gabriel Perroni), visando validar se a implementação estava correta antes de subir as alterações para o repositório.
- **Avaliação e Ajustes (Troubleshooting):** A resposta da IA foi satisfatória, servindo para confirmar que o código estava correto e pronto para o `commit`, evitando erros na esteira do projeto sem necessidade de retrabalho.

### Uso de IA — Validação dos Testes do Cálculo de Custo e do Stage de Build (Leonardo Vieira)
Estes são os detalhes do uso da IA como apoio de validação:
- **Ferramenta Utilizada: Gemini.
- **Prompt e Objetivo: após implementar os testes do serviço CalculadorCusto (casos com mock, sem mock e um negativo) e montar o stage de Build no Jenkinsfile, pedi à IA para validar se a lógica e a sintaxe estavam corretas, se os cenários de teste cobriam bem o serviço e se o uso do mock estava adequado.
- **Avaliação e Ajustes (Troubleshooting): a IA confirmou que a implementação estava correta e apontou pequenos ajustes de sintaxe, que foram revisados e aplicados antes de subir para o repositório.

### Uso de IA — Correção da Suíte de Testes (Leonardo Vieira)
- **Ferramenta Utilizada: Gemini .
- **Prompt e Objetivo: ao rodar a suíte de testes, ela estava quebrando por causa de uma dependência não declarada (freezegun) e de uma fixture inexistente no placeholder do otimizador. Pedi à IA para ajudar a identificar a causa dos erros e confirmar a correção.
- **Avaliação e Ajustes (Troubleshooting): a IA ajudou a localizar os dois problemas, que foram corrigidos (declaração da freezegun no pyproject e ajuste do placeholder), deixando a suíte passando.

### Requisitos Funcionais
Estes são os comportamentos e funcionalidades diretas que o usuário interage:
- **Cadastro e Gestão de Motoristas**: O sistema deve permitir o cadastro de novos motoristas, armazenando dados como nome, CNH e tipo de veículo.
- **Cadastro e Gestão de Entregas:** O sistema deve permitir o registro de novas entregas, incluindo endereços de origem e destino e peso.
- **Monitoramento de Status de Entregas:** O sistema deve listar e atualizar o status das entregas em tempo real.
- **Acompanhamento da Situação dos Motoristas:** O sistema deve permitir listar e visualizar a situação atual dos motoristas.
- **Algoritmo de Otimização de Rotas:** O sistema deve contar com um algoritmo capaz de calcular a rota ideal para maximizar a eficiência de tempo e combustível.
- **Visualização do Mapa:** O sistema deve exibir visualmente em um mapa interativo a rota otimizada gerada para o trajeto dos motoristas.

### Requisitos Não Funcionais

- **Testabilidade**: o sistema usa injeção de dependência nos serviços, o que permite testar as regras de negócio com mocks no lugar dos provedores externos. Os testes não dependem de rede nem de serviços de terceiros.
- **Qualidade de código**: o projeto segue um padrão de estilo verificado por análise estática (flake8), e a pipeline avisa por email quando o lint encontra problemas.
- **(CI/CD):** o projeto tem uma pipeline no Jenkins com os estágios de build, testes (com relatório de cobertura) e deploy, rodando a cada alteração no repositório.
- **Portabilidade**: a aplicação roda em Python 3.11 ou superior e é empacotada com Docker, o que permite subir em qualquer ambiente sem configuração manual.
- **Manutenibilidade**: o código é organizado em camadas (modelos, serviços, interfaces e repositórios), separando os dados das regras de negócio, o que facilita a manutenção e a evolução.
- **Tratamento de erros**: o sistema usa exceções próprias de domínio, deixando claro quando uma regra de negócio foi violada em vez de deixar o erro passar.
- **Disponibilidade**: a aplicação é publicada no Render e fica acessível por uma URL pública.
