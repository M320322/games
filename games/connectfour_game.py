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

    def initial_state(self) -> tuple[np.ndarray, int]:
        """
        Return the initial game state.

        Returns
        -------
        tuple[numpy.ndarray, int]
            Initial state as (board, current_player).
            Board: 0 = empty, 1 = Player 1, -1 = Player 2.
        """
        board = np.zeros((self.board_size, self.board_size), dtype=int)
        return (board, 1)

    def actions(self, state: tuple[np.ndarray, int]) -> list[int]:
        """
        Return a list of valid actions (columns) for the given state.

        Parameters
        ----------
        state : tuple[numpy.ndarray, int]
            The game state as (board, current_player).

        Returns
        -------
        list[int]
            List of valid column indices (0 to board_size-1).
        """
        board, _ = state

        if self.is_terminal(state):
            return []

        valid_mask = board[0, :] == 0
        valid_columns = np.where(valid_mask)[0].tolist()

        return valid_columns

    def next(
        self, state: tuple[np.ndarray, int], action: int
    ) -> tuple[np.ndarray, int]:
        """
        Return the state that results from dropping a piece in the given column.

        Parameters
        ----------
        state : tuple[numpy.ndarray, int]
            The current game state as (board, current_player).
        action : int
            The column to drop the piece into (0 to board_size-1).

        Returns
        -------
        tuple[numpy.ndarray, int]
            The resulting state as (new_board, next_player).

        Raises
        ------
        ValueError
            If the column is full or invalid.
        """
        board, player = state

        if action < 0 or action >= self.board_size:
            raise ValueError(
                f"Invalid column: {action}. Must be 0 to {self.board_size - 1}"
            )

        if board[0][action] != 0:
            raise ValueError(f"Column {action} is full")

        new_board = board.copy()

        column = new_board[:, action]
        empty_positions = np.where(column == 0)[0]
        if len(empty_positions) > 0:
            new_board[empty_positions[-1], action] = player

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
        Check if there's a winner on the board using vectorized matrix operations.

        Parameters
        ----------
        board : numpy.ndarray
            The game board.

        Returns
        -------
        int or None
            The player number (1 or -1) if there's a winner, None otherwise.
        """
        if self.board_size == 4:
            return self._check_4x4_winner(board)
        elif self.board_size == 5:
            for row_offset in range(2):
                for col_offset in range(2):
                    submatrix = board[
                        row_offset : row_offset + 4, col_offset : col_offset + 4
                    ]
                    winner = self._check_4x4_winner(submatrix)
                    if winner is not None:
                        return winner

        return None

    def _check_4x4_winner(self, board_4x4: np.ndarray) -> int | None:
        """
        Check for winner in a 4x4 board using vectorized operations.

        Parameters
        ----------
        board_4x4 : numpy.ndarray
            A 4x4 board section to check.

        Returns
        -------
        int or None
            The player number (1 or -1) if there's a winner, None otherwise.
        """
        lines = np.concatenate(
            [
                board_4x4.sum(axis=1),  # Row sums
                board_4x4.sum(axis=0),  # Column sums
                [np.trace(board_4x4)],  # Main diagonal
                [np.trace(np.fliplr(board_4x4))],  # Anti-diagonal
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

        symbol_map = np.array([".", "X", "", "O"])  # Index: -1->O, 0->., 1->X
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

        if self.is_terminal(self.state):
            winner = self._check_winner(board)
            if winner:
                return f"{board_str}\n\nGame Over! Player {winner} ({'X' if winner == 1 else 'O'}) wins!"
            else:
                return f"{board_str}\n\nGame Over! It's a draw!"
        else:
            return (
                f"{board_str}\n\nPlayer {player}'s turn ({'X' if player == 1 else 'O'})"
                f"\nEnter column (0-{self.board_size - 1}) to drop your piece:"
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

        board_list = board.tolist()

        return {
            "board": board_list,
            "board_size": self.board_size,
            "current_player": player,
            "is_game_over": self.is_game_over(),
            "winner": self._check_winner(board) if self.is_game_over() else None,
            "valid_actions": self.actions(self.state),
        }
