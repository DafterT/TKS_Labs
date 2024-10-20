from socket import *
import threading

def handle_request(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        with open(filename[1:], 'rb') as f:
            outputdata = f.read()
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        connectionSocket.sendall(outputdata)
    except IOError:
        not_found_response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
        connectionSocket.send(not_found_response.encode())
    finally:
        connectionSocket.close()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 80))
    serverSocket.listen(5)

    print('Готов к обслуживанию...')

    while True:
        connectionSocket, addr = serverSocket.accept()
        print(addr)
        client_thread = threading.Thread(target=handle_request, args=(connectionSocket,))
        client_thread.start()

if __name__ == "__main__":
    main()
