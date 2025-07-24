"""
Tic-Tac-Toe game implementation.

Rules:
- 3x3 grid
- Players take turns placing X and O
- First to get 3 in a row (horizontal, vertical, or diagonal) wins
- If the board is full and no winner, it's a draw
"""

import numpy as np
from typing import Any, Tuple, List, Dict, Optional
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

    def initial_state(self) -> Tuple[np.ndarray, int]:
        """
        Return the initial game state.

        Returns
        -------
        Tuple[numpy.ndarray, int]
            Initial state as (board, current_player).
            Board: 0 = empty, 1 = Player 1 (X), -1 = Player -1 (O).
        """
        board = np.zeros((3, 3), dtype=int)
        return (board, 1)

    def actions(self) -> List[Tuple[int, int]]:
        """
        Return a list of valid actions for the given state.

        Returns
        -------
        List[Tuple[int, int]]
            List of valid positions as (row, col) tuples.
        """
        board, _ = self.state

        if self.is_terminal():
            return []

        empty_positions = np.argwhere(board == 0)
        return [(int(row), int(col)) for row, col in empty_positions]

    def next(self, action: Tuple[int, int]) -> None:
        """
        Update the game state to the next state after making an action.

        Parameters
        ----------
        action : Tuple[int, int]
            The action to take as (row, col).

        Raises
        ------
        ValueError
            If the position is already occupied.
        """
        board, player = self.state
        row, col = action

        if board[row][col] != 0:
            raise ValueError(
                f"Invalid move: position ({row}, {col}) is already occupied"
            )

        new_board = board.copy()
        new_board[row, col] = player

        self.state = (new_board, -player)

    def is_terminal(self) -> bool:
        """
        Return True if the game is over in the given state.

        Returns
        -------
        bool
            True if there's a winner or the board is full, False otherwise.
        """
        board, _ = self.state

        if self.get_winner() is not None:
            return True

        return not np.any(board == 0)

    def utility(self) -> float:
        """
        Return the utility value in the terminal state.

        Returns
        -------
        float
            1.0 if Player 1 wins, -1.0 if Player 1 loses, 0.0 for a draw.
        """
        if not self.is_terminal():
            raise ValueError("Game is not over yet")

        winner = self.get_winner()

        if winner:
            return float(winner)
        return 0.0

    def get_winner(self) -> Optional[int]:
        """
        Check if there's a winner on the board.

        Returns
        -------
        Optional[int]
            The player number (1 or -1) if there's a winner, None otherwise.
        """
        board, _ = self.state
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

        if self.is_terminal():
            winner = self.get_winner()
            if winner:
                return f"{board_str}\n\nGame Over! Player {winner} ({'X' if winner == 1 else 'O'}) wins!"
            else:
                return f"{board_str}\n\nGame Over! It's a draw!"
        else:
            return (
                f"{board_str}\n\nPlayer {player}'s turn ({'X' if player == 1 else 'O'})"
            )

    def get_state_display(self) -> Dict[str, Any]:
        """
        Get a display-friendly representation of the state.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing game state information for display.
        """
        board, player = self.state

        board_list = [[int(cell) for cell in row] for row in board]

        return {
            "board": board_list,
            "current_player": player,
            "is_terminal": self.is_terminal(),
            "winner": self.get_winner() if self.is_terminal() else None,
            "valid_actions": self.actions(),
        }
