import socket
import threading
import json
from datetime import datetime
from urllib.parse import parse_qs
from collections import deque

lock = threading.Lock()

def handle_client(client_socket, address):
    print("handling client...")
    try:
        data = client_socket.recv(4096).decode("utf-8", errors="ignore")
        if not data:
            client_socket.close()
            return

        headers, _, body = data.partition("\r\n\r\n")

        request_line = headers.split("\r\n")[0]
        method, path, _ = request_line.split()

        if method == "GET":
            respones_body = f"""

            """

def start_server(host='0.0.0.0', port=8000):
    # start start
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("server started at ", host, ":", port)

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("stopping server...")
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_server()
