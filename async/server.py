import asyncio
import socket
import pickle


class MainServer:
    def __init__(self):
        self.port = 5050
        self.server_hostname = socket.gethostbyname(socket.gethostname())
        self.address = (self.server_hostname, self.port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        self.start_listening()

    def start_listening(self):
        self.server.listen()


if __name__ == '__main__':
    server = MainServer()