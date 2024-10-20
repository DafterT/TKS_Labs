import socket
import time
import random

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('localhost', 12000))

clients = {}

while True:
    rand = random.randint(0, 10)
    message, address = serverSocket.recvfrom(1024)
    message_data = message.decode().split()

    if len(message_data) == 3 and message_data[0] == 'Heartbeat':
        client_id = message_data[1]
        clients[client_id] = time.time()

        print(f"Heartbeat received from client {client_id}")

        # Check for inactive clients
        inactive_clients = [client for client, last_seen in clients.items() if time.time() - last_seen > 5]
        for inactive_client in inactive_clients:
            print(f"Client {inactive_client} is inactive. Application may have stopped.")
            del clients[inactive_client]

    if rand >= 4:
        serverSocket.sendto(message, address)
