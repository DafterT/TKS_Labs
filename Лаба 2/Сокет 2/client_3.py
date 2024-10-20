import socket
import time
import random

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddress = ('localhost', 12000)
client_id = str(random.randint(1, 1000))

while True:
    heartbeat_message = f'Heartbeat {client_id} {time.time()}'
    clientSocket.sendto(heartbeat_message.encode(), serverAddress)
    time.sleep(2)

    sequence_number = random.randint(1, 1000)
    ping_message = f'Ping {sequence_number} {time.time()}'

    try:
        clientSocket.sendto(ping_message.encode(), serverAddress)
        start_time = time.time()
        response, server = clientSocket.recvfrom(1024)
        end_time = time.time()
        rtt = end_time - start_time
        print(f'Response from {server}: {response.decode()} time={rtt:.6f} seconds')

    except socket.timeout:
        print(f'Request timed out')

