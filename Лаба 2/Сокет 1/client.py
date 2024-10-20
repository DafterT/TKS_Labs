import sys
from socket import *

def http_client(server_host, server_port, file_path):
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        request = f"GET {file_path} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
        client_socket.send(request.encode())
        response = client_socket.recv(4096).decode()
        print(response)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python client.py <server_host> <server_port> <file_path>")
        sys.exit(1)
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    file_path = sys.argv[3]
    http_client(server_host, server_port, file_path)
