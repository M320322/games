"""
Human agent that takes input from command line.
"""

from typing import TYPE_CHECKING
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

        actions = game.actions(game.state)

        if not actions:
            return None

        if hasattr(game, "HalvingGame") or game.__class__.__name__ == "HalvingGame":
            return self._choose_halving_action(actions)
        elif (
            hasattr(game, "TicTacToeGame") or game.__class__.__name__ == "TicTacToeGame"
        ):
            return self._choose_tictactoe_action(actions)
        else:
            return self._choose_generic_action(actions)

    def _choose_halving_action(self, actions: list[str]) -> str:
        """
        Choose action for halving game.

        Parameters
        ----------
        actions : list[str]
            List of valid actions for the halving game.

        Returns
        -------
        str
            The chosen action.
        """
        print("Available actions:")
        for i, action in enumerate(actions):
            if action == "subtract":
                print(f"{i + 1}. Subtract 1")
            elif action == "halve":
                print(f"{i + 1}. Divide by 2")

        while True:
            try:
                choice = int(input("Enter your choice (number): ")) - 1
                if 0 <= choice < len(actions):
                    return actions[choice]
                else:
                    print(f"Please enter a number between 1 and {len(actions)}")
            except ValueError:
                print("Please enter a valid number")

    def _choose_tictactoe_action(
        self, actions: list[tuple[int, int]]
    ) -> tuple[int, int]:
        """
        Choose action for tic-tac-toe game.

        Parameters
        ----------
        actions : list[tuple[int, int]]
            List of valid positions as (row, col) tuples.

        Returns
        -------
        tuple[int, int]
            The chosen position as (row, col).
        """
        print("Available positions:")
        for i, (row, col) in enumerate(actions):
            print(f"{i + 1}. Row {row + 1}, Column {col + 1}")

        while True:
            try:
                choice = int(input("Enter your choice (number): ")) - 1
                if 0 <= choice < len(actions):
                    return actions[choice]
                else:
                    print(f"Please enter a number between 1 and {len(actions)}")
            except ValueError:
                print("Please enter a valid number")

    def _choose_generic_action(self, actions: list[any]) -> any:
        """
        Choose action for any game.

        Parameters
        ----------
        actions : list[any]
            List of valid actions for the current game.

        Returns
        -------
        any
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
