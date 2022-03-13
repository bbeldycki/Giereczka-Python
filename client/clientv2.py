import pickle
import select
import socket
import traceback
import sys
import pygame
from settings import *


class Game:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((SERVER_IP, SERVER_PORT))
        self.header = 1024
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('My Game')
        self.clock = pygame.time.Clock()
        self.id = None

    def run(self) -> None:
        while True:
            ready_socket, _, _ = select.select([self.server], [], [], CLIENT_TIMEOUT)
            try:
                if ready_socket:
                    data = pickle.loads(self.server.recv(self.header))

                    if self.id is None and isinstance(data, dict):
                        self.id = data['players'][0]['id']
                        print(f'id: {self.id}')

                    while True:
                        self.clock.tick_busy_loop(FPS)
                        response = {'commands': [], 'id': self.id}
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                response['commands'].append({'quit_game': {'quit_game': True, 'id': self.id}})
                                print(response)
                                self.server.send(pickle.dumps({'action': 'commands', 'value': response}))
                                pygame.quit()
                                sys.exit()

            except Exception as e:
                print('global error: ' + str(e))
                self.server.send(pickle.dumps({'action': 'error', 'value': {'error': e}}))
                traceback.print_exc()
                exit()


if __name__ == '__main__':
    game = Game()
    game.run()
