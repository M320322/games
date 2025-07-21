"""
Games package containing all game implementations.
"""

from .base_game import Game
from .halving_game import HalvingGame
from .tictactoe_game import TicTacToeGame
from .nim_game import NimGame
from .connectfour_game import ConnectFourGame

__all__ = ["Game", "HalvingGame", "TicTacToeGame", "NimGame", "ConnectFourGame"]
