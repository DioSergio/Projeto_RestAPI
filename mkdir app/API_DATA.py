from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sqlite3

#URL da API - endpoint
url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#Parametros de requisição
parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD'
}
#Cabecalho - define o tipo de dado e a chave da API usada
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '59a3f197-0d08-405c-a205-50543f5b3ed1',
}

session = Session()
session.headers.update(headers)

def request_data():
  try:
    #Requisição dos dados do servidor
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return data['data']
  except Exception as e:
    print('Erro ao buscar dados:', e)
    return [];

# cria tabela no SQLite
def create_table():
  con = sqlite3.connect('coins.db')
  cursor = con.cursor()

  cursor.execute('''
  CREATE TABLE IF NOT EXISTS coins(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      simbolo TEXT NOT NULL,
      preco REAL,
      marketcap REAL,
      volume24h REAL
  )
  ''')
  con.commit()
  con.close()

# Salva dados no banco
def save_db(coins):
  con = sqlite3.connect('coins.db')
  cursor = con.cursor()
  for coin in coins:
    cursor.execute('''
      INSERT OR REPLACE INTO coins (id, nome, simbolo, preco, marketcap, volume24h)
VALUES (?, ?, ?, ?, ?, ?)
    ''', (
      coin['id'],
      coin['nome'],
      coin['simbolo'],
      coin['preco'],
      coin['marketcap'],
      coin['volume24h'],
    ))
  con.commit()
  con.close()

#Executa as funções acima
def main():
  create_table()
  raw_data = request_data()
  formatted_data = []

  for coin in raw_data:
    formatted_data.append({
      'id': coin['id'],
      'nome': coin['name'],
      'simbolo': coin['symbol'],
      'preco': coin['quote']['USD']['price'],
      'marketcap': coin['quote']['USD']['market_cap'],
      'volume24h': coin['quote']['USD']['volume_24h']
    })

  save_db(formatted_data)
  print("Dados salvos com sucesso!")

if __name__ == '__main__':
    main()