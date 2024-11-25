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
    print("Client connected address: %s:%i" % (new_conn[1][0], new_conn[1][1]))         # выведем адресс клиента
    new_socket = new_conn[0]
    
    data = b''                                                              # читаем пока не найдем пустую строку
    while b'\r\n\r\n' not in data:
        chunk = new_socket.recv(4096)
        data+=chunk
    headers, _, payload = data.decode("ISO-8859-1").partition("\r\n\r\n")   # разбиваем на заголовок и тело
    
    content_length = 0                                                      # найдем ожидаему длину тела
    for line in headers.split("\r\n"):
        if line.lower().startswith("Content-Length:"):
            content_length = int(line.split(":")[1].strip())

    payload_len = len(payload)                                              # если фактическая длина тела меньше ожидаемой, то 
    if payload_len < content_length:                                        # считаем еще, пока не получим полностью
        while payload_len < content_length:
            chunk = new_socket.recv(4096)
            payload += chunk
            payload_len = len(payload)
    
    request_method = headers.split()[0]
    print("Client request method:", request_method)
    print("Client payload:", payload)
                                       
    response = (
        "HTTP/1.1 200 OK\r\n"                   # простейший ответ http сервера
        "Content-Type: text/plain\r\n"
        "Content-Length: 6\r\n"
        "Connection: close\r\n"
        "\r\n"
        "Hello!"
    )
    
    new_socket.sendall(response.encode("ISO-8859-1"))
    new_socket.close()
    