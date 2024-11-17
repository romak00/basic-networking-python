import socket
import sys

host= sys.argv[1]   # читаем имя хоста и порт 
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # создаем объект сокета, первый параметр говорит что используем IPv4
s.connect((host, port))                                 # второй - то что используем TCP

request = "GET / HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n" % (host)    # стандартный хедер реквеста, в конце пустая строка
encoded_request = request.encode("ISO-8859-1")                                  # стандартная веб кодировка
s.sendall(encoded_request)

response = b""
while True:
    chunk = s.recv(4096)        # читаем чанками до 4096 байт за раз
    if not chunk:
        break
    response += chunk

s.close()

decoded_response = response.decode("ISO-8859-1")
print(decoded_response)