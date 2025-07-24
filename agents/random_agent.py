"""
Random agent that chooses actions randomly.
"""

import random
from typing import TYPE_CHECKING
from .base_agent import Agent

if TYPE_CHECKING:
    from games.base_game import Game


class RandomAgent(Agent):
    """
    Agent that chooses actions randomly.

    Parameters
    ----------
    player_id : int
        The ID of the player (1 or -1).
    name : str, default="Random AI"
        The display name for the agent.
    random_seed : int, default=42
        Random seed for reproducibility.
    """

    def __init__(
        self, player_id: int, name: str = "Random AI", random_seed: int = 42
    ) -> None:
        super().__init__(player_id, name)
        self.random_seed = random_seed
        random.seed(self.random_seed)

    def choose_action(self, game: "Game") -> any:
        """
        Choose a random action from available actions.

        Parameters
        ----------
        game : Game
            The current game instance.

        Returns
        -------
        any
            A randomly chosen action from the valid actions, or None if no actions available.
        """
        actions = game.actions()

        if not actions:
            return None

        action = random.choice(actions)
        print(f"{self.name} chooses: {action}")
        return action
