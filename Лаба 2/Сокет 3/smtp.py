from socket import *
import base64

mas = "\r\nI love Computer Networks"
endmsg = "\r\n.\r\n"

mailserver = ("aspmx.l.google.com", 25)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024).decode("utf-8")
print(f"Message after connection request: {recv}")
if recv[:3] != "220":
    print("220 reply not received from server.")

hello_command = "HELO Alice\r\n"
clientSocket.send(hello_command.encode())
recv1 = clientSocket.recv(1024).decode("utf-8")
print(recv1)
if recv[:3] != "250":
    print("250 reply not received from server.")

username = "ilia.jurav@gmail.com"
password = "Jurav1480"
base64_str = f"\x00{username}\x00{password}".encode()
base64_str = base64.b64encode(base64_str)
auth_msg = "AUTH PLAIN".encode() + base64_str + "\r\n".encode()
clientSocket.send(auth_msg)
if recv[:3] != "250":
    print("250 reply not received from server.")

mail_from = "MAIL FROM: <ilia.jurav@gmail.com> \r\n"
clientSocket.send(mail_from.encode())
recv2 = clientSocket.recv(1024).decode("utf-8")
print(f"After MAIL FROM command: {recv2}")
if recv[:3] != "250":
    print("250 reply not received from server.")

rcpt_to = "RCPT TO: <ilia.jurav@gmail.com> \r\n"
clientSocket.send(rcpt_to.encode())
recv3 = clientSocket.recv(1024).decode("utf-8")
print(f"After RCPT TO command: {recv3}")
if recv[:3] != "250":
    print("250 reply not received from server.")

data = "DATA\r\n"
clientSocket.send(data.encode())
recv4 = clientSocket.recv(1024).decode("utf-8")
print(f"After DATA command: {recv4}")
if recv[:3] != "250":
    print("250 reply not received from server.")

subject = "Subject: SMTP mail client testing \r\n\t\n"
clientSocket.send(subject.encode())
message = "1234567"
clientSocket.send(message.encode())
clientSocket.send(endmsg.encode())
recv_msg = clientSocket.recv(1024).decode("utf-8")
print("Response after sending message body: ", recv_msg)
if recv[:3] != "250":
    print("250 reply not received from server.")

clientSocket.send("QUIT\r\n".encode())
message = clientSocket.recv(1024).decode("utf-8")
print(f'Message = "{message}"')
clientSocket.close()
