# Проверил, что представлял из себя порт 1025.
# В такой реализации конечно ничего не работает))
import socket

with socket.socket() as sock:
    sock.bind(('', 1025))
    sock.listen(1)
    conn, addr = sock.accept()
    with conn:
        print('connected by: ', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # conn.send(data.upper())
