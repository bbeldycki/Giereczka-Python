import pickle
import select
import socket
import traceback
import sys
import pygame

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5050
CLIENT_TIMEOUT = 0.001

WIDTH = 800
HEIGHT = 600


class Game:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((SERVER_IP, SERVER_PORT))
        self.header = 1024
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('My Game')
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        while True:
            ready_socket, _, _ = select.select([self.server], [], [], CLIENT_TIMEOUT)
            try:
                if ready_socket:
                    try:
                        data = pickle.loads(self.server.recv(self.header))
                    except:
                        continue

                    print(data)
            except Exception as e:
                print('global error: ' + str(e))
                self.server.send(pickle.dumps({'action': 'error', 'value': {'error': e}}))
                traceback.print_exc()
                exit()


if __name__ == '__main__':
    game = Game()
    game.run()
