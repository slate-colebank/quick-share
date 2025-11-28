import socket
import threading
import json
from datetime import datetime
from urllib.parse import parse_qs
from collections import deque


paste_text = "" # holds the content of the text window

# handle a client connection
def handle_client(client_socket, address):
    print("handling client...")
    global paste_text
    try:
        data = client_socket.recv(4096).decode("utf-8", errors="ignore")
        if not data:
            client_socket.close()
            return

        headers, _, body = data.partition("\r\n\r\n")

        request_line = headers.split("\r\n")[0]
        method, path, _ = request_line.split()

        # access the webpage
        if method == "GET":
            page = f"""
            <html>
            <body>
                <form method="POST">
                    <textarea name="text" style="width:50%;height:95vh;">{paste_text}</textarea>
                    <br>
                    <button type="submit">Save</button>
                </form>
            </body>
            </html>
            """

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(page.encode())}\r\n"
                "Connection: close\r\n"
                "\r\n" +
                page
            )
            client_socket.sendall(response.encode())
            return

        # update the contents of the text window (server side)
        if method == "POST":
            print("saving...")
            from urllib.parse import parse_qs
            form = parse_qs(body)
            paste_text = form.get("text", [""])[0]

            response = (
                "HTTP/1.1 303 See Other\r\n"
                "Location: /\r\n"
                "Connection: close\r\n\r\n"
            )
            client_socket.sendall(response.encode())
            return

    except Exception as e:
        print("error:", e)
    finally:
        client_socket.close()

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
