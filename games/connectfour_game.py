"""
Connect Four game implementation.

Rules:
- Choose between 4x4 or 5x5 grid
- Players take turns dropping pieces into columns
- Pieces fall to the lowest available position in a column
- First to get 4 in a row (horizontal, vertical, or diagonal) wins
- If the board is full and no winner, it's a draw
"""

import numpy as np
from typing import Any, Tuple, List, Dict, Optional
from .base_game import Game


class ConnectFourGame(Game):
    """
    Implementation of Connect Four.

    Attributes
    ----------
    board_size : int
        Size of the square board (4 or 5).
    board : numpy.ndarray
        NxN array representing the game board (0=empty, 1=Player 1, -1=Player 2).
    """

    def __init__(self, board_size: int = 4) -> None:
        """
        Initialize Connect Four game.

        Parameters
        ----------
        board_size : int, optional
            Size of the square board (4 or 5), by default 4.

        Raises
        ------
        ValueError
            If board_size is not 4 or 5.
        """
        if board_size not in [4, 5]:
            raise ValueError("Board size must be 4 or 5")

        self.board_size = board_size
        super().__init__()

    def initial_state(self) -> Tuple[np.ndarray, int]:
        """
        Return the initial game state.

        Returns
        -------
        Tuple[numpy.ndarray, int]
            Initial state as (board, current_player).
            Board: 0 = empty, 1 = Player 1, -1 = Player 2.
        """
        board = np.zeros((self.board_size, self.board_size), dtype=int)
        return (board, 1)

    def actions(self) -> List[int]:
        """
        Return a list of valid actions (columns).

        Returns
        -------
        List[int]
            List of valid column indices (0 to board_size-1).
        """
        board, _ = self.state

        if self.is_terminal():
            return []

        valid_mask = board[0, :] == 0
        valid_columns = np.where(valid_mask)[0].tolist()

        return valid_columns

    def next(self, action: int) -> None:
        """
        Update the game state by applying the action.

        Parameters
        ----------
        action : int
            The column to drop the piece into (0 to board_size-1).

        Raises
        ------
        ValueError
            If the column is full or invalid.
        """
        board, player = self.state

        if action < 0 or action >= self.board_size:
            raise ValueError(
                f"Invalid column: {action}. Must be 0 to {self.board_size - 1}"
            )

        if board[0, action] != 0:
            raise ValueError(f"Column {action} is full")

        new_board = board.copy()

        # Find the lowest empty row in the column
        column = new_board[:, action]
        empty_positions = np.where(column == 0)[0]
        if len(empty_positions) > 0:
            new_board[empty_positions[-1], action] = player

        self.state = (new_board, -player)

    def is_terminal(self) -> bool:
        """
        Return True if the game is over in the current state.

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
        Return the utility in the terminal state.

        Returns
        -------
        float
            1.0 if Player 1 wins, -1.0 if Player 1 loses, 0.0 for a draw.
        """
        if not self.is_terminal():
            raise ValueError("Game is not over yet")

        if (winner := self.get_winner()) is None:
            return 0.0
        return float(winner)

    def get_winner(self) -> Optional[int]:
        """
        Check if there's a winner on the board.

        Returns
        -------
        Optional[int]
            The player ID (1 or -1) if there's a winner, None otherwise.
        """
        if self.board_size == 4:
            return self._get_4x4_winner()
        elif self.board_size == 5:
            return self._get_5x5_winner()
        return None

    def _get_4x4_winner(self) -> Optional[int]:
        """
        Check for winner in a 4x4 board.

        Returns
        -------
        Optional[int]
            The player ID (1 or -1) if there's a winner, None otherwise.
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

        if 4 in lines:
            return 1
        elif -4 in lines:
            return -1

        return None

    def _get_5x5_winner(self) -> Optional[int]:
        """
        Check for winner in a 5x5 board.

        Returns
        -------
        Optional[int]
            The player ID (1 or -1) if there's a winner, None otherwise.
        """
        board, _ = self.state
        board_flip = np.fliplr(board)
        board_diag = np.diagonal(board, offset=0)
        board_diag_flip = np.diagonal(board_flip, offset=0)
        lines = np.concatenate(
            [
                board[:, :4].sum(axis=1),  # Row sums
                board[:, 1:].sum(axis=1),  # Row sums shifted
                board[:4, :].sum(axis=0),  # Column sums
                board[1:, :].sum(axis=0),  # Column sums shifted
                [np.trace(board, offset=1)],
                [np.trace(board, offset=-1)],
                [np.trace(board_flip, offset=1)],
                [np.trace(board_flip, offset=-1)],
                [np.sum(board_diag[:4])],
                [np.sum(board_diag[1:])],
                [np.sum(board_diag_flip[:4])],
                [np.sum(board_diag_flip[1:])],
            ]
        )

        if 4 in lines:
            return 1
        elif -4 in lines:
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

        symbol_map = np.array([".", "X", "", "O"])
        display_indices = np.where(board == -1, 3, board)
        symbol_board = symbol_map[display_indices]

        lines = []

        col_numbers = " " + " ".join(str(i) for i in range(self.board_size))
        lines.append(col_numbers)
        lines.append("-" * len(col_numbers))

        for i in range(self.board_size):
            row = "|" + "|".join(symbol_board[i, :]) + "|"
            lines.append(row)

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
                f"\nEnter column (0-{self.board_size - 1}) to drop your piece:"
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

        board_list = board.tolist()

        return {
            "board": board_list,
            "board_size": self.board_size,
            "current_player": player,
            "is_terminal": self.is_terminal(),
            "winner": self.get_winner() if self.is_terminal() else None,
            "valid_actions": self.actions(),
        }
