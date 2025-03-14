# proj_licita_bot

## Descrição
O **proj_licita_bot** é um projeto que realiza a extração de dados do **Portal Nacional de Contratações Públicas (PNCP)** e os armazena em um banco de dados **MongoDB** para facilitar análises e consultas posteriores.

## Objetivo
O projeto visa obter dados do **PNCP** relacionados a processos de contratação pública e salvar essas informações em um banco de dados, permitindo uma melhor análise e organização dos registros.

## Funcionalidades
- **Consulta de contratos**: Obtém contratos publicados no portal.
- **Consulta de contratações publicadas**: Recupera registros de contratações realizadas.
- **Filtragem de editais**: Consulta e extrai informações sobre editais específicos.
- **Armazenamento no MongoDB**: Os dados extraídos são salvos para consultas futuras.

## Estrutura do Projeto

O projeto contém os seguintes arquivos principais:

### `pncp_api.py`
Este arquivo contém a classe `Pncp`, responsável por interagir com a API do **PNCP**. Ele permite consultas para obter contratos, contratações publicadas e editais.

### `db_mongo.py`
Gerencia a conexão com o **MongoDB** e contém a função `sintetiza_bruto()`, que aplica filtros nos dados extraídos e formata os registros para análises.

### `alimentador.py`
Executa as consultas na API e armazena os dados no banco **MongoDB**. Ele coleta as informações brutas e, posteriormente, sintetiza os dados para facilitar a análise.

## Requisitos
Para utilizar o projeto, é necessário ter instalado:
- **Python 3.8+**
- **MongoDB** (Local ou MongoDB Atlas)
- Pacotes Python:
  - `requests`
  - `pymongo`
  - `python-dotenv`
  - `locale`

## Configuração
Antes de rodar o projeto, é necessário configurar o acesso ao banco **MongoDB**.

1. Criar um arquivo `.env` na raiz do projeto e adicionar a variável `MONGO_PASS` com a senha do banco de dados:
   ```ini
   MONGO_PASS=sua_senha_aqui
   ```
2. Modificar o código no arquivo `db_mongo.py` para apontar para o seu próprio banco **MongoDB** caso utilize um servidor diferente.

## Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute a extração de dados brutos:
   ```bash
   python alimentador.py
   ```
3. Os dados filtrados podem ser consultados executando:
   ```bash
   python db_mongo.py
   ```

## Contribuição
Caso queira utilizar este projeto para seu próprio propósito, basta modificar as variáveis necessárias para que apontem para o seu banco **MongoDB**.

Sugestões e melhorias são bem-vindas!
