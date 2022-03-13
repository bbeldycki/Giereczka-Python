import select
import socket
import threading
import pickle
import time
from client.settings import *
from typing import Dict, Any
import sys


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

    @staticmethod
    def _handle_quit_game(status: Dict[str, Any], command: Dict[str, Any]) -> Dict[str, Any]:
        for player in status['players']:
            if player['id'] == command['id']:
                status['quit_game'] = command['quit_game']
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
            print(f'[ACTIVE PLAYERS COUNT] {self.active_player_count}')

    def run(self) -> None:
        while True:
            try:
                client, address = self.server.accept()
                self.__total_player_count += 1

                self._establish_connection(self, address, time.time())

                connection_thread = threading.Thread(target=self._handler, args=(client, address, self.status))
                connection_thread.start()
                print(f'[ACTIVE PLAYERS COUNT] {self.active_player_count}')
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                self.socket.close()
                sys.exit()
            except BaseException as error:
                print(f'[SERVER EXCEPTION] {error}')
                self.socket.close()
                sys.exit()

    def _handler(self, connection: socket.socket, address: tuple, status: Dict[str, Any]) -> None:
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
                    if status['quit_game']:
                        self._client_disconnected(address, time.time())
                        break
                    else:
                        connection.send(pickle.dumps(status))
                else:
                    print(f'NO HANDLER FOR {response["action"]}')
            except Exception as e:
                print(f'[EXCEPTION] {e}')
                break

    @staticmethod
    def _establish_connection(self, address: tuple, connection_time: float) -> None:
        print(f'CONNECTION HAS BEEN ESTABLISHED WITH: {address} at {connection_time}.')
        self.status['players'].append(
            {
                'id': str(self.__total_player_count),
                'pos': (WIDTH / 2, HEIGHT / 2),
                'dir': 1,
                'stats': initialize_stats()
            }
        )

    @staticmethod
    def _client_disconnected(address: tuple, disconnection_time: float) -> None:
        print(f'CLIENT WITH {address} HAS BEEN DISCONNECTED at {disconnection_time}.')

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
