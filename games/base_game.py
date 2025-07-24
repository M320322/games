"""
Base game class for all games in the repository.
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Optional


class Game(ABC):
    """
    Abstract base class for all games.

    Attributes
    ----------
    state : any
        The current game state.
    """

    def __init__(self) -> None:
        self.state = self.initial_state()

    @abstractmethod
    def initial_state(self) -> Any:
        """
        Return the initial game state.

        Returns
        -------
        Any
            The initial state of the game.
        """
        pass

    def initial_player(self) -> int:
        """
        Return the first player to move (always 1).

        Returns
        -------
        int
            The player ID of the first player.
        """
        return 1

    @abstractmethod
    def actions(self) -> list:
        """
        Return a list of valid actions for the current state.

        Returns
        -------
        list
            List of valid actions for the current state.
        """
        pass

    @abstractmethod
    def next(self, action: Any) -> None:
        """
        Update the game state to the next state after making an action.

        Parameters
        ----------
        action : Any
            The action to take.
        """
        pass

    @abstractmethod
    def is_terminal(self) -> bool:
        """
        Return True if the game is over.

        Returns
        -------
        bool
            True if the game is over, False otherwise.
        """
        pass

    @abstractmethod
    def utility(self) -> float:
        """
        Return the utility value in the terminal state.

        Returns
        -------
        float
            The utility value.
        """
        pass

    @abstractmethod
    def get_winner(self) -> Optional[int]:
        """
        Get the winner of the game if it's over.

        Returns
        -------
        int or None
            The player ID of the winner (1 or -1), 0 for draw, or None if game is not over.
        """
        pass

    def copy(self) -> "Game":
        """
        Return a deep copy of the game.

        Returns
        -------
        Game
            A deep copy of the current game instance.
        """
        return deepcopy(self)

    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of the current game state.

        Returns
        -------
        str
            Human-readable representation of the game state.
        """
        pass
