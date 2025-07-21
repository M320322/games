"""
Nim game implementation.

Rules:
- Multiple piles of objects (stones, matches, etc.)
- Players take turns removing any number of objects from a single pile
- The player who takes the last object wins (normal play)
- Default setup: 4 piles with 1, 3, 5, 7 objects respectively
"""

import numpy as np
from .base_game import Game


class NimGame(Game):
    """
    Implementation of the Nim game.

    Parameters
    ----------
    piles : list[int], default=[1, 3, 5, 7]
        Initial number of objects in each pile.

    Attributes
    ----------
    initial_piles : list[int]
        The initial pile configuration.
    """

    def __init__(self, piles: list[int] = None) -> None:
        if piles is None:
            piles = [1, 3, 5, 7]
        self.initial_piles = piles.copy()
        super().__init__()

    def initial_state(self) -> tuple[list[int], int]:
        """
        Return the initial game state.

        Returns
        -------
        tuple[list[int], int]
            Initial game state as (piles, current_player).
            piles: list of integers representing objects in each pile.
        """
        return (self.initial_piles.copy(), 1)

    def actions(self, state: tuple[list[int], int]) -> list[tuple[int, int]]:
        """
        Return a list of valid actions for the given state.

        Parameters
        ----------
        state : tuple[list[int], int]
            The game state as (piles, current_player).

        Returns
        -------
        list[tuple[int, int]]
            List of valid actions as (pile_index, objects_to_remove).
            Each action represents removing a number of objects from a specific pile.
        """
        piles, _ = state
        piles_array = np.array(piles)

        non_empty_mask = piles_array > 0
        non_empty_indices = np.where(non_empty_mask)[0]
        non_empty_sizes = piles_array[non_empty_mask]

        pile_indices_list = []
        removal_counts_list = []

        for i, (pile_idx, pile_size) in enumerate(
            zip(non_empty_indices, non_empty_sizes)
        ):
            removals = np.arange(1, pile_size + 1)
            pile_indices = np.full(len(removals), pile_idx)

            pile_indices_list.append(pile_indices)
            removal_counts_list.append(removals)

        if pile_indices_list:
            all_pile_indices = np.concatenate(pile_indices_list)
            all_removal_counts = np.concatenate(removal_counts_list)

            actions = list(zip(all_pile_indices.tolist(), all_removal_counts.tolist()))
        else:
            actions = []

        return actions

    def next(
        self, state: tuple[list[int], int], action: tuple[int, int]
    ) -> tuple[list[int], int]:
        """
        Return the state that results from making an action in the given state.

        Parameters
        ----------
        state : tuple[list[int], int]
            The current game state as (piles, current_player).
        action : tuple[int, int]
            The action to take as (pile_index, objects_to_remove).

        Returns
        -------
        tuple[list[int], int]
            The resulting state as (new_piles, next_player).

        Raises
        ------
        ValueError
            If the action is invalid.
        """
        piles, player = state
        pile_idx, objects_to_remove = action

        if pile_idx < 0 or pile_idx >= len(piles):
            raise ValueError(f"Invalid pile index: {pile_idx}")

        if objects_to_remove < 1 or objects_to_remove > piles[pile_idx]:
            raise ValueError(
                f"Invalid number of objects to remove: {objects_to_remove}"
            )

        new_piles = piles.copy()
        new_piles[pile_idx] -= objects_to_remove
        next_player = -player

        return (new_piles, next_player)

    def is_terminal(self, state: tuple[list[int], int]) -> bool:
        """
        Return True if the game is over in the given state.

        Parameters
        ----------
        state : tuple[list[int], int]
            The game state as (piles, current_player).

        Returns
        -------
        bool
            True if all piles are empty (game is over), False otherwise.
        """
        piles, _ = state
        return all(pile == 0 for pile in piles)

    def utility(self, state: tuple[list[int], int], player: int) -> float:
        """
        Return the utility value for the given player in the terminal state.

        Parameters
        ----------
        state : tuple[list[int], int]
            The terminal game state as (piles, current_player).
        player : int
            The player ID to evaluate utility for.

        Returns
        -------
        float
            The utility value for the player (1 if won, -1 if lost).
            In Nim, the player who made the last move wins.
        """
        if not self.is_terminal(state):
            return 0.0

        _, current_player = state
        previous_player = -current_player

        if player == previous_player:
            return 1.0  # Win
        else:
            return -1.0  # Loss

    def player(self, state: tuple[list[int], int]) -> int:
        """
        Return the player whose turn it is in the given state.

        Parameters
        ----------
        state : tuple[list[int], int]
            The game state as (piles, current_player).

        Returns
        -------
        int
            The player ID whose turn it is (1 or -1).
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
        piles, current_player = self.state

        result = "Nim Game State:\n"
        for i, pile in enumerate(piles):
            result += f"Pile {i + 1}: {'*' * pile} ({pile})\n"

        if self.is_terminal(self.state):
            winner = self.get_winner()
            if winner is not None:
                winner_symbol = "Player 1" if winner == 1 else "Player -1"
                result += f"Game Over! Winner: {winner_symbol}"
        else:
            player_symbol = "Player 1" if current_player == 1 else "Player -1"
            result += f"Current player: {player_symbol}"

        return result

    def get_nim_sum(self, state: tuple[list[int], int] = None) -> int:
        """
        Calculate the nim-sum (XOR of all pile sizes) for the given state.

        This is useful for optimal strategy - a nim-sum of 0 means the current
        player is in a losing position (assuming perfect play).

        Parameters
        ----------
        state : tuple[list[int], int], optional
            The game state to evaluate. If None, uses current state.

        Returns
        -------
        int
            The nim-sum of all piles.
        """
        if state is None:
            state = self.state

        piles, _ = state
        return np.bitwise_xor.reduce(np.array(piles))

    def get_optimal_move(
        self, state: tuple[list[int], int] = None
    ) -> tuple[int, int] | None:
        """
        Get the optimal move for the current position using nim-sum strategy.

        Parameters
        ----------
        state : tuple[list[int], int], optional
            The game state to evaluate. If None, uses current state.

        Returns
        -------
        tuple[int, int] or None
            The optimal move as (pile_index, objects_to_remove), or None if
            no winning move exists (nim-sum is already 0).
        """
        if state is None:
            state = self.state

        piles, _ = state
        piles_array = np.array(piles)
        nim_sum = self.get_nim_sum(state)

        if nim_sum == 0:
            return None

        targets = np.bitwise_xor(piles_array, nim_sum)
        valid_moves = targets < piles_array

        if np.any(valid_moves):
            pile_idx = np.argmax(valid_moves)
            target = targets[pile_idx]
            objects_to_remove = piles_array[pile_idx] - target
            return (int(pile_idx), int(objects_to_remove))

        return None

    def get_state_display(self) -> dict[str, any]:
        """
        Get a display-friendly representation of the state.

        Returns
        -------
        dict[str, any]
            Dictionary containing game state information for display.
        """
        piles, current_player = self.state
        return {
            "piles": piles,
            "current_player": current_player,
            "is_game_over": self.is_game_over(),
            "winner": self.get_winner() if self.is_game_over() else None,
            "valid_actions": self.actions(self.state),
            "nim_sum": self.get_nim_sum(),
            "optimal_move": self.get_optimal_move(),
            "total_objects": sum(piles),
        }
