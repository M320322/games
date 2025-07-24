"""
Minimax agent that uses the minimax algorithm to choose optimal actions.
"""

import random
from typing import TYPE_CHECKING
from .base_agent import Agent

if TYPE_CHECKING:
    from games.base_game import Game


class MinimaxAgent(Agent):
    """
    Agent that uses minimax algorithm to choose actions.

    Parameters
    ----------
    player_id : int
        The ID of the player (1 or -1).
    name : str, default="Minimax AI"
        The display name for the agent.
    random_seed : int, default=42
        Random seed for reproducibility.
    """

    def __init__(
        self, player_id: int, name: str = "Minimax AI", random_seed: int = 42
    ) -> None:
        super().__init__(player_id, name)
        self.random_seed = random_seed
        random.seed(self.random_seed)

    def choose_action(self, game: "Game") -> any:
        """
        Choose the best action using minimax algorithm.

        Parameters
        ----------
        game : Game
            The current game instance.

        Returns
        -------
        any
            The optimal action according to minimax algorithm, or None if no actions available.
        """
        actions = game.actions()

        if not actions:
            return None

        if len(actions) == 1:
            action = actions[0]
            print(f"{self.name} chooses: {action}")
            return action

        # Store all actions
        action_values = []
        for action in actions:
            game_copy = game.copy()
            game_copy.next(action)
            value = self._minimizer(game_copy)
            action_values.append((action, value))

        max_value = max(action_values, key=lambda x: x[1])[1]
        best_actions = [action for action, value in action_values if value == max_value]

        # Randomly choose among the best actions
        best_action = random.choice(best_actions)

        print(f"{self.name} chooses: {best_action} (value: {max_value:.2f})")
        return best_action

    def _maximizer(self, game: "Game") -> float:
        if game.is_terminal():
            return self.player_id * game.utility()

        max_eval = float("-inf")
        for action in game.actions():
            game_copy = game.copy()
            game_copy.next(action)
            eval_score = self._minimizer(game_copy)
            max_eval = max(max_eval, eval_score)
        return max_eval

    def _minimizer(self, game: "Game") -> float:
        if game.is_terminal():
            return self.player_id * game.utility()

        min_eval = float("inf")
        for action in game.actions():
            game_copy = game.copy()
            game_copy.next(action)
            eval_score = self._maximizer(game_copy)
            min_eval = min(min_eval, eval_score)
        return min_eval
