# UDPPingerServer.py
# Следующий модуль используется для генерирования случайных потерь пакетов
import random
from socket import *
# Создаем UDP-сокет
# Для UDP используем SOCK_DGRAM
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Связываем порт 12000 с сокетом сервера
serverSocket.bind(('', 12000))
while True:
    # Генерируем случайное число от 0 до 10
    rand = random.randint(0, 10)
    # Получаем пакеты от клиента с адресом address
    message, address = serverSocket.recvfrom(1024)
    # Делаем символы клиентского сообщения заглавными
    message = message.upper()
    # Если rand меньше 4, считаем пакет потерянным и не выдаем ответ
    if rand < 4:
        continue
    # В противном случае сервер дает ответ
    serverSocket.sendto(message, address)
