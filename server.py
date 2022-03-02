import socket
import threading
import pickle
import sys

header = 64
formatter = 'utf-8'
disconnect_message = 'disconnect'
server = socket.gethostbyname(socket.gethostname())
port = 5050
addr = (server, port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)


def handle_client(connection, address):
    print(f'[NEW CONNECTION] {address} connected.')

    connected = True
    while connected:
        msg_length = connection.recv(header).decode(formatter)
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(formatter)
            if msg == disconnect_message:
                connected = False
            print(f'[{address}] {msg}')
            connection.send('Msg received'.encode(formatter))
    connection.close()


def handle_client_pickle(connection, address):
    print(f'[NEW CONNECTION] {address} connected.')

    connected = True
    while connected:
        msg_received = connection.recv(1024)
        if msg_received:
            msg = pickle.loads(msg_received)
            if msg.get('disconnects', False):
                connected = False
            print(f'[{address}] {msg}')
            connection.send(pickle.dumps('Message received!'))
    connection.close()


def start():
    s.listen()
    print(f'[LISTENING] Server is listening on {server}')
    while True:
        connection, address = s.accept()
        thread = threading.Thread(target=handle_client_pickle, args=(connection, address))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


print('[STARTING] server is starting...')
start()
