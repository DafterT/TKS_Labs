import os
import struct
import sys
import time
from socket import *

import select

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = string[count + 1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xFFFFFFFF
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xFFFFFFFF

    csum = (csum >> 16) + (csum & 0xFFFF)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xFFFF
    answer = answer >> 8 | (answer << 8 & 0xFF00)
    return answer


def build_packet():
    myChecksum = 0
    myID = os.getpid() & 0xFFFF
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)
    if sys.platform == "darwin":
        myChecksum = htons(myChecksum) & 0xFFFF
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet


def get_route(hostname):
    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)
            icmp = getprotobyname("icmp")
            with socket(AF_INET, SOCK_RAW, icmp) as mySocket:
                mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack("I", ttl))
                mySocket.settimeout(TIMEOUT)
                try:
                    d = build_packet()
                    mySocket.sendto(d, (hostname, 0))
                    t = time.time()
                    startedSelect = time.time()
                    whatReady = select.select([mySocket], [], [], timeLeft)
                    howLongInSelect = time.time() - startedSelect
                    if whatReady[0] == []:  # Timeout
                        print(" * * * Request timed out.")
                    recvPacket, addr = mySocket.recvfrom(1024)
                    timeReceived = time.time()
                    timeLeft = timeLeft - howLongInSelect
                    if timeLeft <= 0:
                        print(" * * * Request timed out.")
                except timeout:
                    continue
                else:
                    try:
                        intermediate_host = gethostbyaddr(addr[0])[0]
                    except herror:
                        intermediate_host = "Unknown"
                    icmpHeader = recvPacket[20:28]
                    types, code, checksum, packetID, sequence = struct.unpack(
                        "bbHHh", icmpHeader
                    )
                    if types in (3, 11, 0):
                        bytes = struct.calcsize("d")
                        timeSent = struct.unpack("d", recvPacket[28 : 28 + bytes])[0]
                        rtt = (timeReceived - t) * 1000
                        print(f" {ttl} rtt={rtt:.0f} ms {addr[0]} {intermediate_host}")
                        if types == 0:
                            return
                    else:
                        print("error")
                        break


get_route("google.com")
