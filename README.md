
# CRUD de Criptomoedas com CoinMarketCap

Este projeto realiza um CRUD (Create, Read, Update, Delete) de criptomoedas utilizando dados da API do CoinMarketCap e uma API REST personalizada feita em Python.

## Objetivos

- Buscar dados da API CoinMarketCap.
- Armazenar os dados em um banco SQLite.
- Criar uma API REST personalizada usando `http.server` e `socketserver`.
- Manipular os dados via requisições HTTP (GET, POST, PUT, DELETE).
- Utilizar apenas bibliotecas padrão do Python e `requests`.

## Estrutura do Projeto

- `fetch_data.py`: busca os dados do CoinMarketCap e insere no banco de dados SQLite.
- `server.py`: implementa um servidor HTTP com rotas REST para manipular os dados das criptomoedas.
- `coins.db`: banco de dados SQLite contendo as criptomoedas.
- `README.md`: instruções do projeto.

## Como Usar

1. Instale a biblioteca `requests`:
   ```
   pip install requests
   ```

2. Execute o script para buscar e salvar os dados:
   ```
   python fetch_data.py
   ```

3. Inicie o servidor:
   ```
   python server.py
   ```

4. Teste a API usando `curl`, `Postman` ou qualquer cliente HTTP:

### Exemplos de Requisições

- **GET /coins**: lista todas as criptomoedas  
- **GET /coins/{id}**: busca uma criptomoeda por ID  
- **POST /coins**: adiciona uma nova criptomoeda  
- **PUT /coins/{id}**: atualiza os dados de uma criptomoeda  
- **DELETE /coins/{id}**: remove uma criptomoeda

### Exemplo com `curl`

```bash
curl http://localhost:8000/coins

curl -X POST http://localhost:8000/coins \
  -H "Content-Type: application/json" \
  -d '{"nome": "NovaCoin", "simbolo": "NVC", "preco": 1.23, "marketcap": 1000000, "volume24h": 50000}'

curl -X PUT http://localhost:8000/coins/1 \
  -H "Content-Type: application/json" \
  -d '{"nome": "Atualizada", "simbolo": "ATD", "preco": 2.50, "marketcap": 2000000, "volume24h": 70000}'

curl -X DELETE http://localhost:8000/coins/1
```

## Banco de Dados

Tabela `coins`:

- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `nome` (TEXT)
- `simbolo` (TEXT)
- `preco` (REAL)
- `marketcap` (REAL)
- `volume24h` (REAL)
