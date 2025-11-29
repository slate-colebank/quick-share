import os
import re
import socket
import threading
import requests
import json
from datetime import datetime
from urllib.parse import parse_qs
from collections import deque


paste_text = "" # holds the content of the text window
uploaded_files = [] # holds the current uploaded files

# handle file upload
# def handle_file_upload(client_socket, raw_data):
def handle_file_upload(headers, body, client_socket):
    m = re.search(r"boundary=(.+)", headers)
    if not m:
        return

    boundary = m.group(1)
    parts = body.split("--" + boundary)

    filename = None
    file_bytes = None

    for part in parts:
        if 'Content-Disposition:' in part and 'filename=' in part:

            # get filename
            name_match = re.search(r'filename="(.?)"', part)
            if name_match:
                filename = name_match.group(1)

            # get data
            if "\r\n\r\n" in part:
                file_data = part.split("\r\n\r\n", 1)[1]

                file_data = file_data.rsplit("\r\n", 1)[0]

                file_bytes = file_data.encode("latin1", errors="ignore")

        if not filename or file_bytes is None:
            return

        with open(filename, "wb") as f:
            f.write(file_bytes)

    uploaded_files.append(filename)

    print(f"Uploaded: {filename}")

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(page.encode())}\r\n"
        "Connection: close\r\n"
        "\r\n" +
        page
    )
    client_socket.sendall(response.encode())


# handle a client connection
def handle_client(client_socket, address):
    print("handling client...")
    global paste_text
    try:
        # Read raw data as bytes first
        raw_data = client_socket.recv(8192)
        if not raw_data:
            client_socket.close()
            return

        # Parse headers only
        header_end = raw_data.find(b"\r\n\r\n")
        headers = raw_data[:header_end].decode("utf-8", errors="ignore")
        
        request_line = headers.split("\r\n")[0]
        method, path, _ = request_line.split()

        # Handle file upload
        if method == "POST" and path == "/upload":
            if "Content-Type: multipart/form-data" in headers:
                handle_file_upload(headers, raw_data, client_socket)
                return

        # For non-file requests, decode body as text
        body = raw_data[header_end + 4:].decode("utf-8", errors="ignore")

        # access the webpage
        if method == "GET":
            page = """
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                    }
                    .container {
                        display: flex;
                        height: 70vh;
                    }
                    .left-half {
                        width: 50%;
                        background-color: #f0f0f0;
                        padding: 20px;
                    }
                    .right-half {
                        width: 50%;
                        background-color: #f0f0f0;
                        padding: 20px;
                    }
                </style>
            </head>
            <body>
                <h1>Quickshare</h1>
                <div class="container">
                    <div class="left-half">
                        <h2>Text</h2>
                        <form method="POST">
                            <textarea name="text" style="width:100%;height:75vh;">{paste_text}</textarea>
                            <br>
                            <button type="submit">Save</button>
                        </form>
                    </div>
                    <div class="right-half">
                        <h2>Files</h2>
                        <form method="POST" enctype="multipart/form-data" action="/upload">
                            <input type="file" name="file">
                            <br><br>
                            <button type="submit">Upload</button>
                        </form>
                    </div>
                </div>
            </body>
            </html>
            """

            page = page.replace("{paste_text}", paste_text)

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
