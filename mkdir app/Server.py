import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
from urllib.parse import urlparse, parse_qs

DB_NAME = 'coins.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

class CoinManager(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        conn = get_db_connection()
        cursor = conn.cursor()

        if len(path_parts) == 1 and path_parts[0] == 'coins':
            # Listar todas
            cursor.execute("SELECT * FROM coins")
            result = [dict(row) for row in cursor.fetchall()]
            self._send_response(200, result)

        elif len(path_parts) == 2 and path_parts[0] == 'coins':
            # Buscar por ID
            try:
                crypto_id = int(path_parts[1])
                cursor.execute("SELECT * FROM coins WHERE id = ?", (crypto_id,))
                row = cursor.fetchone()
                if row:
                    self._send_response(200, dict(row))
                else:
                    self._send_response(404, {"error": "Criptomoeda não encontrada"})
            except ValueError:
                self._send_response(400, {"error": "ID inválido"})
        else:
            self._send_response(404, {"error": "Rota não encontrada"})

        conn.close()

    def do_POST(self):
        if self.path != '/coins':
            self._send_response(404, {"error": "Rota não encontrada"})
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        data = json.loads(body)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO coins (nome, simbolo, preco, marketcap, volume24h)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['nome'], data['simbolo'], data['preco'],
            data['marketcap'], data['volume24h']
        ))
        conn.commit()
        conn.close()
        self._send_response(201, {"message": "Criptomoeda adicionada com sucesso"})

    def do_PUT(self):
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) != 2 or path_parts[0] != 'coins':
            self._send_response(404, {"error": "Rota não encontrada"})
            return

        try:
            crypto_id = int(path_parts[1])
        except ValueError:
            self._send_response(400, {"error": "ID inválido"})
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        data = json.loads(body)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE coins
            SET nome = ?, simbolo = ?, preco = ?, marketcap = ?, volume24h = ?
            WHERE id = ?
        ''', (
            data['nome'], data['simbolo'], data['preco'],
            data['marketcap'], data['volume24h'],
            crypto_id
        ))
        conn.commit()
        conn.close()
        self._send_response(200, {"message": "Criptomoeda atualizada com sucesso"})

    def do_DELETE(self):
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) != 2 or path_parts[0] != 'coins':
            self._send_response(404, {"error": "Rota não encontrada"})
            return

        try:
            crypto_id = int(path_parts[1])
        except ValueError:
            self._send_response(400, {"error": "ID inválido"})
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM coins WHERE id = ?', (crypto_id,))
        conn.commit()
        conn.close()
        self._send_response(200, {"message": "Criptomoeda removida com sucesso"})

    def _send_response(self, status_code, content):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode('utf-8'))

#Inicia o servidor
if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(("", PORT), CoinManager) as httpd:
        print(f"Servidor rodando em http://localhost:{PORT}")
        httpd.serve_forever()
#578