"""
Tic-Tac-Toe game implementation.

Rules:
- 3x3 grid
- Players take turns placing X and O
- First to get 3 in a row (horizontal, vertical, or diagonal) wins
- If the board is full and no winner, it's a draw
"""

import numpy as np
from .base_game import Game


class TicTacToeGame(Game):
    """
    Implementation of Tic-Tac-Toe.

    Attributes
    ----------
    board : numpy.ndarray
        3x3 array representing the game board (0=empty, 1=X, -1=O).
    """

    def __init__(self) -> None:
        super().__init__()

    def initial_state(self) -> tuple[np.ndarray, int]:
        """
        Return the initial game state.

        Returns
        -------
        tuple[numpy.ndarray, int]
            Initial state as (board, current_player).
            Board: 0 = empty, 1 = Player 1 (X), -1 = Player -1 (O).
        """
        board = np.zeros((3, 3), dtype=int)
        return (board, 1)

    def actions(self, state: tuple[np.ndarray, int]) -> list[tuple[int, int]]:
        """
        Return a list of valid actions for the given state.

        Parameters
        ----------
        state : tuple[numpy.ndarray, int]
            The game state as (board, current_player).

        Returns
        -------
        list[tuple[int, int]]
            List of valid positions as (row, col) tuples.
        """
        board, _ = state

        if self.is_terminal(state):
            return []

        empty_positions = np.argwhere(board == 0)
        return [(int(row), int(col)) for row, col in empty_positions]

    def next(
        self, state: tuple[np.ndarray, int], action: tuple[int, int]
    ) -> tuple[np.ndarray, int]:
        """
        Return the state that results from making an action in the given state.

        Parameters
        ----------
        state : tuple[numpy.ndarray, int]
            The current game state as (board, current_player).
        action : tuple[int, int]
            The action to take as (row, col).

        Returns
        -------
        tuple[numpy.ndarray, int]
            The resulting state as (new_board, next_player).

        Raises
        ------
        ValueError
            If the position is already occupied.
        """
        board, player = state
        row, col = action

        if board[row][col] != 0:
            raise ValueError(
                f"Invalid move: position ({row}, {col}) is already occupied"
            )

        new_board = board.copy()
        new_board[row][col] = player

        next_player = -player
        return (new_board, next_player)

    def is_terminal(self, state: tuple[np.ndarray, int]) -> bool:
        """
        Return True if the game is over in the given state.

        Parameters
        ----------
        state : tuple[numpy.ndarray, int]
            The game state as (board, current_player).

        Returns
        -------
        bool
            True if there's a winner or the board is full, False otherwise.
        """
        board, _ = state

        if self._check_winner(board) is not None:
            return True

        return not np.any(board == 0)

    def utility(self, state: tuple[np.ndarray, int], player: int) -> float:
        """
        Return the utility value for the given player in the terminal state.

        Parameters
        ----------
        state : tuple[numpy.ndarray, int]
            The terminal game state as (board, current_player).
        player : int
            The player ID to evaluate utility for.

        Returns
        -------
        float
            1.0 if the player wins, 0.0 for draw, -1.0 if the player loses.
        """
        if not self.is_terminal(state):
            return 0

        board, _ = state
        winner = self._check_winner(board)

        if winner == player:
            return 1  # Win
        elif winner is None:
            return 0  # Draw
        else:
            return -1  # Loss

    def player(self, state: tuple[np.ndarray, int]) -> int:
        """
        Return the player whose turn it is in the given state.

        Parameters
        ----------
        state : tuple[numpy.ndarray, int]
            The game state as (board, current_player).

        Returns
        -------
        int
            The player ID whose turn it is.
        """
        board, current_player = state
        return current_player

    def _check_winner(self, board: np.ndarray) -> int | None:
        """
        Check if there's a winner on the board using efficient numpy operations.

        Parameters
        ----------
        board : numpy.ndarray
            The 3x3 game board.

        Returns
        -------
        int or None
            The player number (1 or -1) if there's a winner, None otherwise.
        """
        lines = np.concatenate(
            [
                board.sum(axis=1),  # Row sums
                board.sum(axis=0),  # Column sums
                [np.trace(board)],  # Main diagonal
                [np.trace(np.fliplr(board))],  # Anti-diagonal
            ]
        )

        if 3 in lines:
            return 1
        elif -3 in lines:
            return -1

        return None

    def __str__(self) -> str:
        """
        String representation of the current game state.

        Returns
        -------
        str
            Human-readable representation of the game board and status.
        """
        board, player = self.state

        symbols = {0: " ", 1: "X", -1: "O"}
        lines = []

        for i in range(3):
            row = "|".join([f" {symbols[board[i][j]]} " for j in range(3)])
            lines.append(row)
            if i < 2:
                lines.append("-----------")

        board_str = "\n".join(lines)

        if self.is_terminal(self.state):
            winner = self._check_winner(board)
            if winner:
                return f"{board_str}\n\nGame Over! Player {winner} ({'X' if winner == 1 else 'O'}) wins!"
            else:
                return f"{board_str}\n\nGame Over! It's a draw!"
        else:
            return (
                f"{board_str}\n\nPlayer {player}'s turn ({'X' if player == 1 else 'O'})"
            )

    def get_state_display(self) -> dict[str, any]:
        """
        Get a display-friendly representation of the state.

        Returns
        -------
        dict[str, any]
            Dictionary containing game state information for display.
        """
        board, player = self.state

        board_list = [[int(cell) for cell in row] for row in board]

        return {
            "board": board_list,
            "current_player": player,
            "is_game_over": self.is_game_over(),
            "winner": self._check_winner(board) if self.is_game_over() else None,
            "valid_actions": self.actions(self.state),
        }
