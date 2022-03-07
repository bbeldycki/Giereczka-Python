import pickle
import sys
import socket

from settings import *
from level import LevelMy

disconnect_message = 'disconnect'
port = 5050
server = '192.168.1.21'
addr = (server, port)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('My Game')
        self.clock = pygame.time.Clock()
        self.level = LevelMy()

    def run(self):
        while True:
            dt = self.clock.tick_busy_loop(60) * 0.001 * fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    send_pickle({'disconnect': True})
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            player_actual_pos = self.level.player.actual_position
            player_next_pos = self.level.player.next_position
            player_position = {
                'actual_player_position': player_actual_pos,
                'next_player_position': player_next_pos
            }
            send_pickle(player_position)
            server_msg = pickle.loads(client.recv(1024))
            self.level.player.actual_position = server_msg
            # print(player_input)
            # self.clock.tick_busy_loop(fps)


def send_pickle(message):
    msg = pickle.dumps(message)
    client.send(msg)
    # print(pickle.loads(client.recv(1024)))


if __name__ == '__main__':
    client.connect(addr)
    send_pickle({'welcome': 'Hello world!'})
    game = Game()
    game.run()
