import socket
import sys

host = ''           # выбирает любой локальный адрес
port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # убирает ошибку “Address already in use” во время bind()
                                                            # обычно возникает во время краша сервера
s.bind((host, port))
s.listen()

while True:
    new_conn = s.accept()               # возвращает новый сокет в виде объекта socket и адрес клиента в виде (host, port)
    new_socket = new_conn[0]
    
    request = b''
    while True:
        chunk = new_socket.recv(4096)
        request += chunk
        if request.decode("ISO-8859-1").find('\r\n\r\n') != -1:     # тут мы не можем просто итерироваться до момента пока
            break                                                   # получим пустую строку, это происходит только когда
                                                                    # клиент оборвет соединение, но он ждет ответа                               
    response = """HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!"""
                                                        # простейший ответ http сервера
    new_socket.sendall(response.encode("ISO-8859-1"))
    new_socket.close()
    