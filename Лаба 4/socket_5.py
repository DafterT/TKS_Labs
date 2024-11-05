import os
import struct
import time
from socket import *

import select

ICMP_ECHO_REQUEST = 8


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


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    startedSelect = time.time()
    whatReady = select.select([mySocket], [], [], timeLeft)
    howLongInSelect = time.time() - startedSelect
    if whatReady[0] == []:  # Время истекло
        print("Превышен интервал ожидания запроса")
        return None
    timeReceived = time.time()
    recPacket, addr = mySocket.recvfrom(1024)

    leftbytes = recPacket[:-8]
    icmpheader = leftbytes[-8:]
    type, code, checksum, id, seq = struct.unpack("!bbHHh", icmpheader)
    if type != 0 or id != ID:
        print("Echo ответ провален")
        return None
    else:
        ipheader = leftbytes[:20]
        icmpdata_bytes = struct.calcsize("d")
        ttl = struct.unpack("!b", ipheader[8:9])[0]
        timeSend = struct.unpack("!d", recPacket[28:])[0]
        delay = timeReceived - timeSend
        return (icmpdata_bytes, delay, ttl)


def sendOnePing(mySocket, destAddr, ID, seq):
    # Формат заголовка: type (8), code (8), checksum (16), id(16), sequence(16)
    myChecksum = 0
    # Делаем фиктивный заголовок с нулевой контрольной суммой.
    # struct -- Интерпретирует строки как упакованные бинарныеданные
    header = struct.pack("!bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, seq)
    data = struct.pack("!d", time.time())
    # Вычисляем контрольную сумму данных и заголовка.
    myChecksum = checksum(header + data)
    header = struct.pack("!bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, seq)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))


def doOnePing(destAddr, timeout, seq):
    icmp = getprotobyname("icmp")
    # SOCK_RAW – достаточно мощный тип сокета.
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Возвращаем идентификатор текущего процесса
    sendOnePing(mySocket, destAddr, myID, seq)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 означает: Если ответа нет в течение секунды, клиент предполагает, что
    # либо пакет запроса, либо ответный пакет потеряны
    dest = gethostbyname(host)
    print("\nПингуем " + dest + " используя Python:")
    print("")
    loss = timeavg = 0
    totalsend = 5
    minDelay = 1000
    maxDelay = 0
    # Send ping requests to a server separated by approximately one second
    for i in range(0, totalsend):
        recv = doOnePing(dest, timeout, i)
        if recv == None:
            loss += 1
        else:
            tmptime = int(recv[1] * 1000)
            print(
                "От {:} ответ: байты={:} задержка={:}мс TTL={:}".format(
                    dest, recv[0], tmptime, recv[2]
                )
            )
            minDelay = min(tmptime, minDelay)
            maxDelay = max(tmptime, maxDelay)
            timeavg += tmptime
        time.sleep(1)
    print("\n{:} Статистика:".format(dest))
    print(
        "\tПакеты данных: Отправлено = {:}, Получено = {:}, Потери = {:}({:}% Потерь),".format(
            totalsend, totalsend - loss, loss, (int)(loss / totalsend * 100)
        )
    )
    print(
        "Расчетное время задержки (мс):\n\tКратчайшее = {:}ms, Наибольшее = {:}мс, средняя = {:}мс".format(
            minDelay, maxDelay, timeavg // totalsend
        )
    )


ping("www.yandex.com")
