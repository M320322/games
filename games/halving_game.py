"""
Halving Game implementation.

Rules:
- Start with a positive integer number
- Players take turns to either:
  1. Subtract 1 from the current number
  2. Divide the current number by 2 using floor division (always available)
- The player who reduces the number to 0 wins
"""

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

    def initial_state(self) -> tuple[int, int]:
        """
        Return the initial game state.

        Returns
        -------
        tuple[int, int]
            Initial game state as (number, current_player).
        """
        return (self.starting_number, 1)

    def actions(self, state: tuple[int, int]) -> list[str]:
        """
        Return a list of valid actions for the given state.

        Parameters
        ----------
        state : tuple[int, int]
            The game state as (number, current_player).

        Returns
        -------
        list[str]
            List of valid actions ("subtract" and "halve").
        """
        return [] if self.is_terminal(state) else ["subtract", "halve"]

    def next(self, state: tuple[int, int], action: str) -> tuple[int, int]:
        """
        Return the state that results from making an action in the given state.

        Parameters
        ----------
        state : tuple[int, int]
            The current game state as (number, current_player).
        action : str
            The action to take ("subtract" or "halve"). "subtract" reduces the
            number by 1, "halve" divides by 2 using floor division.

        Returns
        -------
        tuple[int, int]
            The resulting state as (new_number, next_player).

        Raises
        ------
        ValueError
            If the action is invalid.
        """
        number, player = state

        if action == "subtract":
            new_number = number - 1
        elif action == "halve":
            new_number = number // 2
        else:
            raise ValueError(f"Invalid action: {action}")

        next_player = -player  # Switch between 1 and -1
        return (new_number, next_player)

    def is_terminal(self, state: tuple[int, int]) -> bool:
        """
        Return True if the game is over in the given state.

        Parameters
        ----------
        state : tuple[int, int]
            The game state as (number, current_player).

        Returns
        -------
        bool
            True if the number is 0 (game over), False otherwise.
        """
        number, _ = state
        return number == 0

    def utility(self, state: tuple[int, int], player: int) -> float:
        """
        Return the utility value for the given player in the terminal state.

        Parameters
        ----------
        state : tuple[int, int]
            The terminal game state as (number, current_player).
        player : int
            The player ID to evaluate utility for.

        Returns
        -------
        float
            1.0 if the player wins, -1.0 if the player loses, 0.0 for non-terminal states.
        """
        if not self.is_terminal(state):
            return 0

        _, last_player = state
        previous_player = -last_player

        if player == previous_player:
            return 1  # Win
        else:
            return -1  # Loss

    def player(self, state: tuple[int, int]) -> int:
        """
        Return the player whose turn it is in the given state.

        Parameters
        ----------
        state : tuple[int, int]
            The game state as (number, current_player).

        Returns
        -------
        int
            The player ID whose turn it is.
        """
        _, current_player = state
        return current_player

    def __str__(self) -> str:
        """
        String representation of the current game state.

        Returns
        -------
        str
            Human-readable representation of the game state.
        """
        number, player = self.state
        if self.is_terminal(self.state):
            winner = -player
            return f"Game Over! Number: {number}, Player {winner} wins!"
        else:
            return f"Number: {number}, Player {player}'s turn"

    def get_state_display(self) -> dict[str, any]:
        """
        Get a display-friendly representation of the state.

        Returns
        -------
        dict[str, any]
            Dictionary containing game state information for display.
        """
        number, player = self.state
        return {
            "number": number,
            "current_player": player,
            "is_game_over": self.is_game_over(),
            "winner": self.get_winner() if self.is_game_over() else None,
            "valid_actions": self.actions(self.state),
        }
