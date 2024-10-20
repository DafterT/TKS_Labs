from socket import *
import sys

# Создаем словарь для хранения кэшированных объектов
cache = {}

if len(sys.argv) <= 2:
    print('Используйте: "python ProxyServer.py server_ip server_port"\n[server_ip – IP-адрес прокси-сервера]')
    sys.exit(2)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], int(sys.argv[2])))
tcpSerSock.listen(100)

while True:
    print('Готов к обслуживанию...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Установлено соединение с:', addr)

    try:
        message = tcpCliSock.recv(1024).decode("utf-8")
        print(message)
        filename = message.split()[1].partition("/")[2]
        print(filename)
        filetouse = "./" + filename

        # Проверяем, есть ли объект в кэше
        if filetouse in cache:
            print('Объект найден в кэше')
            tcpCliSock.send(b'HTTP/1.1 200 OK\n')
            tcpCliSock.send(b'Content-Type: text/html\n\n')
            tcpCliSock.send(cache[filetouse])
        else:
            with open(filetouse[1:], "r") as f:
                outputdata = f.readlines()

            tcpCliSock.send(b'HTTP/1.1 200 OK\n')
            tcpCliSock.send(b'Content-Type: text/html\n\n')

            # Отправляем объект клиенту
            for line in outputdata:
                tcpCliSock.send(line.encode("utf-8"))

            # Кэшируем объект для будущих запросов
            cache[filetouse] = b''.join(outputdata)
            print('Объект добавлен в кэш')

    except FileNotFoundError:
        try:
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            print(hostn)

            c.connect((hostn, 80))
            fileobj = c.makefile('rw')
            fileobj.write("GET http://" + filename + "\n\n")
            fileobj.flush()

            with open(filetouse[1:], "wb") as tmpFile:
                buff = fileobj.readlines()
                for line in buff:
                    tmpFile.write(line.encode("utf-8"))
                    tcpCliSock.send(line.encode("utf-8"))

            c.close()

        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            tcpCliSock.send(b"HTTP/1.1 500 Internal Server Error\r\n")
            tcpCliSock.send(b"Content-Type: text/html\r\n")
            tcpCliSock.send("\r\n")

    tcpCliSock.close()

tcpSerSock.close()
