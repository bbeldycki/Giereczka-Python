from typing import Dict, Any

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5050
SERVER_TIMEOUT = 0.001
CLIENT_TIMEOUT = 0.001

WIDTH = 800
HEIGHT = 600
FPS = 60


def initialize_stats(**kwargs) -> Dict[str, Any]:
    stats = {
        'alive': True,
        'moving': False
    }

    for arg in kwargs:
        stats[arg] = kwargs[arg]

    return stats