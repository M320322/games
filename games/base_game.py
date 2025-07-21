"""
Base game class for all games in the repository.
"""

from abc import ABC, abstractmethod
from copy import deepcopy


class Game(ABC):
    """
    Abstract base class for all games.

    Attributes
    ----------
    state : any
        The current game state.
    current_player : int
        The current player whose turn it is.
    """

    def __init__(self) -> None:
        self.state = self.initial_state()
        self.current_player = self.initial_player()

    @abstractmethod
    def initial_state(self) -> any:
        """
        Return the initial game state.

        Returns
        -------
        any
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
    def actions(self, state: any) -> list:
        """
        Return a list of valid actions for the given state.

        Parameters
        ----------
        state : any
            The game state to evaluate.

        Returns
        -------
        list
            List of valid actions for the given state.
        """
        pass

    @abstractmethod
    def next(self, state: any, action: any) -> any:
        """
        Return the state that results from making an action in the given state.

        Parameters
        ----------
        state : any
            The current game state.
        action : any
            The action to take.

        Returns
        -------
        any
            The resulting game state after taking the action.
        """
        pass

    @abstractmethod
    def is_terminal(self, state: any) -> bool:
        """
        Return True if the game is over in the given state.

        Parameters
        ----------
        state : any
            The game state to evaluate.

        Returns
        -------
        bool
            True if the game is over, False otherwise.
        """
        pass

    @abstractmethod
    def utility(self, state: any, player: int) -> float:
        """
        Return the utility value for the given player in the terminal state.

        Parameters
        ----------
        state : any
            The terminal game state.
        player : int
            The player ID to evaluate utility for.

        Returns
        -------
        float
            The utility value for the player (-1, 0, or 1).
        """
        pass

    @abstractmethod
    def player(self, state: any) -> int:
        """
        Return the player whose turn it is in the given state.

        Parameters
        ----------
        state : any
            The game state to evaluate.

        Returns
        -------
        int
            The player ID whose turn it is (1 or -1).
        """
        pass

    def move(self, action: any) -> any:
        """
        Make a move in the current game state.

        Parameters
        ----------
        action : any
            The action to take.

        Returns
        -------
        any
            The new game state after the move.

        Raises
        ------
        ValueError
            If the action is not valid for the current state.
        """
        if action not in self.actions(self.state):
            raise ValueError(f"Invalid action: {action}")

        self.state = self.next(self.state, action)
        self.current_player = self.player(self.state)

        return self.state

    def is_game_over(self) -> bool:
        """
        Check if the current game is over.

        Returns
        -------
        bool
            True if the game is over, False otherwise.
        """
        return self.is_terminal(self.state)

    def get_winner(self) -> int | None:
        """
        Get the winner of the game if it's over.

        Returns
        -------
        int or None
            The player ID of the winner (1 or -1), 0 for draw, or None if game is not over.
        """
        if not self.is_game_over():
            return None

        # Check utility for each possible player
        for player in [1, -1]:  # Using binary players 1 and -1
            if self.utility(self.state, player) > 0:
                return player
        return 0  # Draw

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
