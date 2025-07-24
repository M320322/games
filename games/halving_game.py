"""
Halving Game implementation.

Rules:
- Start with a positive integer number
- Players take turns to either:
  1. Subtract 1 from the current number
  2. Divide the current number by 2 using floor division (always available)
- The player who reduces the number to 0 wins
"""

from typing import Any, Tuple, List, Dict, Optional
from .base_game import Game


class HalvingGame(Game):
    """
    Implementation of the Halving Game.

    Parameters
    ----------
    starting_number : int, default=15
        The initial number to start the game with.

    Attributes
    ----------
    starting_number : int
        The number the game started with.
    """

    def __init__(self, starting_number: int = 15) -> None:
        self.starting_number = starting_number
        super().__init__()

    def initial_state(self) -> Tuple[int, int]:
        """
        Return the initial game state.

        Returns
        -------
        Tuple[int, int]
            Initial game state as (number, current_player).
        """
        return (self.starting_number, self.initial_player())

    def actions(self) -> List[str]:
        """
        Return a list of valid actions for the current state.

        Returns
        -------
        List[str]
            List of valid actions ("subtract" and "halve").
        """
        return [] if self.is_terminal() else ["subtract", "halve"]

    def next(self, action: str) -> None:
        """
        Update the game state to the next state after making an action.

        Parameters
        ----------
        action : str
            The action to take ("subtract" or "halve"). "subtract" reduces the
            number by 1, "halve" divides by 2 using floor division.

        Raises
        ------
        ValueError
            If the action is invalid.
        """
        number, player = self.state

        if action == "subtract":
            new_number = number - 1
        elif action == "halve":
            new_number = number // 2
        else:
            raise ValueError(f"Invalid action: {action}")

        next_player = -player
        self.state = (new_number, next_player)

    def is_terminal(self) -> bool:
        """
        Return True if the game is over.

        Returns
        -------
        bool
            True if the number is 0 (game over), False otherwise.
        """
        number, _ = self.state
        return number == 0

    def utility(self) -> float:
        """
        Return the utility value in the terminal state.

        Returns
        -------
        float
            1.0 if Player 1 wins, -1.0 if Player 1 loses.
        """
        winner = self.get_winner()

        if winner is None:
            raise ValueError("Game is not over yet")

        return float(winner)

    def get_winner(self) -> Optional[int]:
        """
        Get the winner of the game if it's over.

        Returns
        -------
        Optional[int]
            The player ID of the winner (1 or -1), or None if game is not over.
        """
        if not self.is_terminal():
            return None
        _, current_player = self.state
        return -current_player

    def __str__(self) -> str:
        """
        String representation of the current game state.

        Returns
        -------
        str
            Human-readable representation of the game state.
        """
        number, player = self.state
        if self.is_terminal():
            return f"Game Over! Number: {number}, Player {self.get_winner()} wins!"
        return f"Number: {number}, Player {player}'s turn"

    def get_state_display(self) -> Dict[str, Any]:
        """
        Get a display-friendly representation of the state.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing game state information for display.
        """
        number, player = self.state
        return {
            "number": number,
            "current_player": player,
            "is_terminal": self.is_terminal(),
            "winner": self.get_winner() if self.is_terminal() else None,
            "valid_actions": self.actions(),
        }
