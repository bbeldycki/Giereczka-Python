import pickle
import select
import socket
import traceback
import sys
import pygame
from settings import *
from player import Player


class Game:
    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((SERVER_IP, SERVER_PORT))
        self.header = 1024
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('My Game')
        self.clock = pygame.time.Clock()
        self.id = None
        self.all_sprites = None
        self.main_player = None

    def run(self) -> None:
        while True:
            ready_socket, _, _ = select.select([self.server], [], [], CLIENT_TIMEOUT)
            try:
                if ready_socket:
                    try:
                        data = pickle.loads(self.server.recv(self.header))
                        print(f'receiving data from server: ')
                        print(data)
                    except:
                        continue

                    if self.id is None and isinstance(data, dict):
                        self.id = data['players'][0]['id']
                        print(f'new id: ' + str(self.id))
                        continue
                    elif self.id is not None and not isinstance(data, dict):
                        print(f'data is not a dictionary')
                        continue
                    elif self.id is not None and isinstance(data, dict):
                        players = pygame.sprite.Group()
                        self.all_sprites = pygame.sprite.Group()
                        for player_entity in data['players']:
                            print(player_entity)
                            if player_entity['id'] == self.id:
                                color = (128, 0, 255)
                            else:
                                color = (0, 0, 255)

                            sprite = Player(entity=player_entity, color=color)
                            players.add(sprite)

                            if player_entity['id'] == self.id:
                                self.main_player = sprite
                                self.main_player.main = True

                        self.all_sprites.add(players)

                    else:
                        print(data)
                        exit('strange result:')

                    if self.all_sprites is None:
                        continue
                    else:
                        self.clock.tick_busy_loop(FPS)
                        response = {'commands': [], 'id': self.id}
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                response['commands'].append({'quit_game': {'quit_game': True, 'id': self.id}})
                                print(response)
                                self.server.send(pickle.dumps({'action': 'commands', 'value': response}))
                                pygame.quit()
                                sys.exit()

                        self.all_sprites.update()

                        if self.main_player is not None:
                            if self.main_player.stats['moving']:
                                response['commands'].append({'movement': self.main_player.entity})

                        if len(response['commands']):
                            print(f'sending:')
                            response = {'action': 'commands', 'value': response}
                            print(response)
                            self.server.send(pickle.dumps(response))

            except Exception as e:
                print('global error: ' + str(e))
                self.server.send(pickle.dumps({'action': 'error', 'value': {'error': e}}))
                traceback.print_exc()
                exit()


if __name__ == '__main__':
    game = Game()
    game.run()
