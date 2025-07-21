"""
Base agent class for all AI agents.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from games.base_game import Game


class Agent(ABC):
    """
    Abstract base class for all agents.

    Parameters
    ----------
    player_id : int
        The ID of the player (1 or -1).
    name : str
        The name of the agent.
    """

    def __init__(self, player_id: int, name: str) -> None:
        self.player_id = player_id
        self.name = name

    @abstractmethod
    def choose_action(self, game: "Game") -> any:
        """
        Choose an action given the current game state.

        Parameters
        ----------
        game : Game
            The current game instance.

        Returns
        -------
        any
            The chosen action for the current game state.
        """
        pass

    def __str__(self) -> str:
        """
        String representation of the agent.

        Returns
        -------
        str
            Formatted string with agent name and player ID.
        """
        return f"{self.name} (Player {self.player_id})"
