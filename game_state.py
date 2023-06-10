from enum import Enum

class GameState(Enum):
    """Les games states possibles dans le jeu, hérite de la classe Enum"""
    NOT_STARTED = 0
    GAME_OVER = 1
    ROUND_ACTIVE = 2
    ROUND_DONE = 3