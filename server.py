import select
import socket
import threading
import pickle
import time

from client.server_validate_position import *
from typing import Dict, Any
import sys

# header = 64
# formatter = 'utf-8'
# disconnect_message = 'disconnect'
# server = socket.gethostbyname(socket.gethostname())
# port = 5050
# addr = (server, port)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(addr)
SERVER_TIMEOUT = 0.001
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5050

# def handle_client(connection, address):
#     print(f'[NEW CONNECTION] {address} connected.')
#
#     connected = True
#     while connected:
#         msg_length = connection.recv(header).decode(formatter)
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = connection.recv(msg_length).decode(formatter)
#             if msg == disconnect_message:
#                 connected = False
#             print(f'[{address}] {msg}')
#             connection.send('Msg received'.encode(formatter))
#     connection.close()
#
#
# def handle_client_pickle(connection, address):
#     print(f'[NEW CONNECTION] {address} connected.')
#
#     connected = True
#     while connected:
#         msg_received = connection.recv(1024)
#         if msg_received:
#             msg = pickle.loads(msg_received)
#             print(f'[{address}] {msg}')
#             if msg.get('disconnects', False):
#                 connected = False
#             if msg.get('actual_player_position', [0, 0]) and msg.get('next_player_position', [0, 0]):
#                 if can_move_there(msg.get('next_player_position', [0, 0])):
#                     return_value = msg.get('next_player_position', [0, 0])
#                     connection.send(pickle.dumps(return_value))
#                 else:
#                     return_value = msg.get('next_player_position', [0, 0])
#                     connection.send(pickle.dumps(return_value))
#             # connection.send(pickle.dumps('Message received!'))
#     connection.close()
#
#
# def start():
#     s.listen()
#     print(f'[LISTENING] Server is listening on {server}')
#     while True:
#         connection, address = s.accept()
#         thread = threading.Thread(target=handle_client_pickle, args=(connection, address))
#         thread.start()
#         print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')
#
#
# print('[STARTING] server is starting...')
# start()


class ResponseHandler:
    def handle_commands(self, status: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        for command in response['commands']:
            cmd = list(command.keys())[0]
            handler = getattr(self, f'_handle_{cmd}', None)

            if callable(handler):
                status = handler(status, command[cmd])
            else:
                print(f'[NO HANDLER FOR] {cmd}')
        return status

    @staticmethod
    def _handle_movement(status: Dict[str, Any], command: Dict[str, Any]) -> Dict[str, Any]:
        for player in status['players']:
            if player['id'] == command['id']:
                player['pos'] = command['pos']
                player['dir'] = command['dir']
        return status


class MyServer:
    def __init__(self, host: str, port: int, response_handler: ResponseHandler) -> None:
        self.header = 1024  # default header length
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # server Socket
        self.host = host
        self.port = port
        self.response_handler = response_handler
        self.status = {'working': True, 'players': []}
        self.__total_player_count = 0

        try:
            self.server.bind((host, port))
            self.server.listen()
            self.server.settimeout(5.0)
        except Exception as error:
            print(f'[ERROR IN CREATING SERVER] {error}')
            sys.exit()
        else:
            print(f'[SERVER IS LISTENING] @ {host}:{port}')

    def run(self) -> None:
        while True:
            try:
                client, address = self.server.accept()
                self.__total_player_count += 1

                self._establish_connection(address, time.time())

                connection_thread = threading.Thread(target=self._handler, args=(client, self.status))
                connection_thread.start()
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            except BaseException as error:
                print(f'[SERVER EXCEPTION] {error}')
                self.socket.close()
                sys.exit()

    def _handler(self, connection: socket.socket, status: Dict[str, Any]) -> None:
        while True:
            ready_sockets, _, _ = select.select([connection], [], [], SERVER_TIMEOUT)

            if not ready_sockets:
                connection.send(pickle.dumps(status))
                continue
            # response format:
            # for commands: {'action': 'commands', 'value': {'commands': ...}}
            # for errors: {'action': 'error', 'value': {'error': ...}}
            try:
                response = pickle.loads(connection.recv(self.header))
                handler = getattr(self.response_handler, f'handle_{response["action"]}', None)
                if callable(handler):
                    status = handler(status, response['value'])
                    connection.send(pickle.dumps(status))
                else:
                    print(f'NO HANDLER FOR {response["action"]}')
            except Exception as e:
                print(f'[EXCEPTION] {e}')
                break

    @staticmethod
    def _establish_connection(address: str, connection_time: float) -> None:
        print(f'CONNECTION HAS BEEN ESTABLISHED WITH: {address} at {connection_time}.')

    @property
    def total_player_count(self) -> int:
        return self.__total_player_count

    @property
    def active_player_count(self) -> int:
        return threading.active_count() - 1  # Subtract 1 to remove the main thread


def main() -> None:
    server = MyServer(SERVER_IP, SERVER_PORT, ResponseHandler())
    server.run()


if __name__ == '__main__':
    main()
