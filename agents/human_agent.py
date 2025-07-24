"""
Human agent that takes input from command line.
"""

from typing import TYPE_CHECKING, List, Any
from .base_agent import Agent

if TYPE_CHECKING:
    from games.base_game import Game


class HumanAgent(Agent):
    """
    Agent that takes input from a human player.

    Parameters
    ----------
    player_id : int
        The ID of the player (1 or -1).
    name : str, default="Human"
        The display name for the agent.
    """

    def __init__(self, player_id: int, name: str = "Human") -> None:
        super().__init__(player_id, name)

    def choose_action(self, game: "Game") -> any:
        """
        Choose an action by asking for human input.

        Parameters
        ----------
        game : Game
            The current game instance.

        Returns
        -------
        any
            The action chosen by the human player, or None if no valid actions.
        """
        print(f"\n{game}")
        print(f"\n{self.name}, it's your turn!")

        actions = game.actions()

        if not actions:
            return None

        return self._choose_generic_action(actions)

    def _choose_generic_action(self, actions: List[Any]) -> Any:
        """
        Choose action for any game.

        Parameters
        ----------
        actions : List[Any]
            List of valid actions for the current game.

        Returns
        -------
        Any
            The chosen action.
            The chosen action.
        """
        print("Available actions:")
        for i, action in enumerate(actions):
            print(f"{i + 1}. {action}")

        while True:
            try:
                choice = int(input("Enter your choice (number): ")) - 1
                if 0 <= choice < len(actions):
                    return actions[choice]
                else:
                    print(f"Please enter a number between 1 and {len(actions)}")
            except ValueError:
                print("Please enter a valid number")
