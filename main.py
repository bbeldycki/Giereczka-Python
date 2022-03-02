import pickle
import pygame
import sys
import socket

from settings import *
from level import Level

header = 64
formatter = 'utf-8'
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
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # send(disconnect_message)
                    # send_pickle({'disconnect': True})
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick_busy_loop(fps)


# def send(message):
#     msg = message.encode(formatter)
#     msg_length = len(msg)
#     send_length = str(msg_length).encode(formatter)
#     send_length += b' ' * (header - len(send_length))
#     client.send(send_length)
#     client.send(msg)
#     print(client.recv(2048).decode(formatter))
#
#
# def send_pickle(message):
#     msg = pickle.dumps(message)
#     client.send(msg)
#     print(pickle.loads(client.recv(1024)))


if __name__ == '__main__':
    # client.connect(addr)
    # send_pickle({'welcome': 'Hello world!'})
    game = Game()
    game.run()
