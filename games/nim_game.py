"""
Nim game implementation.

Rules:
- Multiple piles of objects (stones, matches, etc.)
- Players take turns removing any number of objects from a single pile
- The player who takes the last object wins (normal play)
- Default setup: 4 piles with 1, 3, 5, 7 objects respectively
"""

from typing import Any, List, Tuple, Dict, Optional
import numpy as np
from .base_game import Game


class NimGame(Game):
    """
    Implementation of the Nim game.

    Parameters
    ----------
    piles : List[int], default=[1, 3, 5, 7]
        Initial number of objects in each pile.

    Attributes
    ----------
    initial_piles : List[int]
        The initial pile configuration.
    """

    def __init__(self, piles: Optional[List[int]] = None) -> None:
        if piles is None:
            piles = [1, 3, 5, 7]
        self.initial_piles = piles.copy()
        super().__init__()

    def initial_state(self) -> Tuple[List[int], int]:
        """
        Return the initial game state.

        Returns
        -------
        Tuple[List[int], int]
            Initial game state as (piles, current_player).
            piles: list of integers representing objects in each pile.
        """
        return (self.initial_piles.copy(), 1)

    def actions(self) -> List[Tuple[int, int]]:
        """
        Return a list of valid actions for the current state.

        Returns
        -------
        List[Tuple[int, int]]
            List of valid actions as (pile_index, objects_to_remove).
            Each action represents removing a number of objects from a specific pile.
        """
        piles, _ = self.state
        piles_array = np.array(piles, dtype=int)

        non_empty_mask = piles_array > 0
        non_empty_indices = np.where(non_empty_mask)[0]
        non_empty_sizes = piles_array[non_empty_mask]

        pile_indices_list = []
        removal_counts_list = []

        for i, (pile_idx, pile_size) in enumerate(
            zip(non_empty_indices, non_empty_sizes)
        ):
            removals = np.arange(1, pile_size + 1, dtype=int)
            pile_indices = np.full(len(removals), pile_idx, dtype=int)

            pile_indices_list.append(pile_indices)
            removal_counts_list.append(removals)

        if pile_indices_list:
            all_pile_indices = np.concatenate(pile_indices_list)
            all_removal_counts = np.concatenate(removal_counts_list)

            actions = list(zip(all_pile_indices.tolist(), all_removal_counts.tolist()))
        else:
            actions = []

        return actions

    def next(self, action: Tuple[int, int]) -> None:
        """
        Update the game state to the next state after making an action.

        Parameters
        ----------
        action : Tuple[int, int]
            The action to take as (pile_index, objects_to_remove).

        Raises
        ------
        ValueError
            If the action is invalid.
        """
        piles, player = self.state
        pile_idx, objects_to_remove = action

        if pile_idx < 0 or pile_idx >= len(piles):
            raise ValueError(f"Invalid pile index: {pile_idx}")

        if objects_to_remove < 1 or objects_to_remove > piles[pile_idx]:
            raise ValueError(
                f"Invalid number of objects to remove: {objects_to_remove}"
            )

        new_piles = piles.copy()
        new_piles[pile_idx] -= objects_to_remove

        self.state = (new_piles, -player)

    def is_terminal(self) -> bool:
        """
        Return True if the game is over in the current state.

        Returns
        -------
        bool
            True if all piles are empty (game is over), False otherwise.
        """
        piles, _ = self.state
        return all(pile == 0 for pile in piles)

    def utility(self) -> float:
        """
        Return the utility value in the terminal state.

        Returns
        -------
        float
            The utility value for Player 1 (1 if won, -1 if lost).
            In Nim, the player who made the last move wins.
        """
        if not self.is_terminal():
            raise ValueError("Game is not over yet")

        return float(self.get_winner())

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
        piles, current_player = self.state

        result = "Nim Game State:\n"
        for i, pile in enumerate(piles):
            result += f"Pile {i + 1}: {'*' * pile} ({pile})\n"

        if self.is_terminal():
            winner = self.get_winner()
            if winner is not None:
                winner_name = "Player 1" if winner == 1 else "Player -1"
                result += f"Game Over! Winner: {winner_name}"
        else:
            player_name = "Player 1" if current_player == 1 else "Player -1"
            result += f"Current player: {player_name}"

        return result

    def get_state_display(self) -> Dict[str, Any]:
        """
        Get a display-friendly representation of the state.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing game state information for display.
        """
        piles, current_player = self.state
        return {
            "piles": piles,
            "current_player": current_player,
            "is_terminal": self.is_terminal(),
            "winner": self.get_winner() if self.is_terminal() else None,
            "valid_actions": self.actions(),
            "total_objects": sum(piles),
        }
