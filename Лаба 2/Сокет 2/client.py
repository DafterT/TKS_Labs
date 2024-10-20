import socket
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
timeout = 1
clientSocket.settimeout(timeout)
serverAddress = ('localhost', 12000)

for sequence_number in range(1, 11):
    message = f'Ping {sequence_number} {time.time()}'
    try:
        clientSocket.sendto(message.encode(), serverAddress)
        start_time = time.time()
        response, server = clientSocket.recvfrom(1024)
        end_time = time.time()
        rtt = end_time - start_time
        print(f'Response from {server}: {response.decode()} RTT={rtt:.6f} seconds')

    except socket.timeout:
        print(f'Request timed out')
clientSocket.close()
