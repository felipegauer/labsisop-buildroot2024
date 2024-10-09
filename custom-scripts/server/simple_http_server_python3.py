import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

HOST_NAME = '0.0.0.0'  # Escutar em todas as interfaces
PORT_NUMBER = 8000

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")  # Definir UTF-8
        s.end_headers()
        
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")  # Definir UTF-8
        s.end_headers()
        
        # Coletar informações do /proc
        uptime = open("/proc/uptime").read().split()[0]
        cpu_info = open("/proc/cpuinfo").readlines()
        mem_info = open("/proc/meminfo").readlines()
        
        # Responder com as informações coletadas
        s.wfile.write("<html><head><title>Servidor Web</title></head>".encode('utf-8'))
        s.wfile.write("<body><h1>Informações do Sistema</h1>".encode('utf-8'))
        s.wfile.write(f"<p>Uptime: {uptime} segundos</p>".encode('utf-8'))
        
        # Exibir algumas informações do /proc/cpuinfo
        for line in cpu_info:
            if "model name" in line or "cpu MHz" in line:
                s.wfile.write(f"<p>{line}</p>".encode('utf-8'))
        
        # Exibir informações de memória
        s.wfile.write("<h2>Memória</h2>".encode('utf-8'))
        for line in mem_info[:5]:  # Mostrar as primeiras 5 linhas
            s.wfile.write(f"<p>{line}</p>".encode('utf-8'))

        s.wfile.write("</body></html>".encode('utf-8'))

if __name__== '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print(f"Servidor iniciado em {HOST_NAME}:{PORT_NUMBER}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(f"Servidor finalizado em {HOST_NAME}:{PORT_NUMBER}")