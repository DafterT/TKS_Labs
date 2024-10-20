import socket
import time

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
timeout = 1
clientSocket.settimeout(timeout)
serverAddress = ('localhost', 12000)

rtt_times = []
lost_packets = 0

for sequence_number in range(1, 11):
    message = f'Ping {sequence_number} {time.time()}'

    try:
        clientSocket.sendto(message.encode(), serverAddress)
        start_time = time.time()
        response, server = clientSocket.recvfrom(1024)
        end_time = time.time()
        rtt = end_time - start_time
        rtt_times.append(rtt)
        print(f'Response from {server}: {response.decode()} time={rtt:.6f} seconds')

    except socket.timeout:
        lost_packets += 1
        print(f'Request timed out')

if rtt_times:
    print(f'--- Ping statistics ---')
    print(f'10 packets transmitted, {len(rtt_times)} packets received, {lost_packets / 10 * 100:.1f}% packet loss')
    print(f'Min/Max/Avg RTT = {min(rtt_times):.6f}/{max(rtt_times):.6f}/{sum(rtt_times) / len(rtt_times):.6f} seconds')

clientSocket.close()
