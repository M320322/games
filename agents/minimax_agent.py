"""
Minimax agent that uses the minimax algorithm to choose optimal actions.
"""

import math
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
    max_depth : int or None, default=None
        Maximum search depth. If None, searches to terminal states.

    Attributes
    ----------
    max_depth : int or None
        The maximum depth to search in the game tree.
    """

    def __init__(
        self, player_id: int, name: str = "Minimax AI", max_depth: int | None = None
    ) -> None:
        super().__init__(player_id, name)
        self.max_depth = max_depth

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
        actions = game.actions(game.state)

        if not actions:
            return None

        if len(actions) == 1:
            action = actions[0]
            print(f"{self.name} chooses: {action}")
            return action

        best_action = None
        best_value = -math.inf

        for action in actions:
            # Create a copy of the game and make the move
            game_copy = game.copy()
            game_copy.move(action)

            # Calculate the minimax value
            value = self._minimax(game_copy, 0, False, -math.inf, math.inf)

            if value > best_value:
                best_value = value
                best_action = action

        print(f"{self.name} chooses: {best_action} (value: {best_value:.2f})")
        return best_action

    def _minimax(
        self,
        game: "Game",
        depth: int,
        maximizing_player: bool,
        alpha: float,
        beta: float,
    ) -> float:
        """
        Minimax algorithm with alpha-beta pruning.

        Parameters
        ----------
        game : Game
            The current game state.
        depth : int
            Current search depth.
        maximizing_player : bool
            True if maximizing player's turn, False if minimizing player's turn.
        alpha : float
            Alpha value for alpha-beta pruning.
        beta : float
            Beta value for alpha-beta pruning.

        Returns
        -------
        float
            The minimax value of the current position.
        """
        if game.is_game_over() or (self.max_depth and depth >= self.max_depth):
            return game.utility(game.state, self.player_id)

        if maximizing_player:
            max_eval = -math.inf
            for action in game.actions(game.state):
                game_copy = game.copy()
                game_copy.move(action)
                eval_score = self._minimax(game_copy, depth + 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return max_eval
        else:
            min_eval = math.inf
            for action in game.actions(game.state):
                game_copy = game.copy()
                game_copy.move(action)
                eval_score = self._minimax(game_copy, depth + 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return min_eval
