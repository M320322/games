"""
Command line interface for running games.
"""

from games import HalvingGame, TicTacToeGame, NimGame, ConnectFourGame
from agents import HumanAgent, RandomAgent, MinimaxAgent, Agent
from games.base_game import Game


def get_agent_choice(player_num: int) -> Agent:
    """
    Get agent type choice from user.

    Parameters
    ----------
    player_num : int
        The player number (1 or -1).

    Returns
    -------
    Agent
        The chosen agent instance.
    """
    display_num = 1 if player_num == 1 else 2
    print(f"\nChoose agent type for Player {display_num}:")
    print("1. Human")
    print("2. Random AI")
    print("3. Minimax AI")

    while True:
        try:
            choice = int(input("Enter your choice (1-3): "))
            if choice == 1:
                return HumanAgent(player_num)
            elif choice == 2:
                return RandomAgent(player_num)
            elif choice == 3:
                return MinimaxAgent(player_num)
            else:
                print("Please enter 1, 2, or 3")
        except ValueError:
            print("Please enter a valid number")


def play_game(game: Game, agent1: Agent, agent2: Agent) -> None:
    """
    Play a game between two agents.

    Parameters
    ----------
    game : Game
        The game instance to play.
    agent1 : Agent
        The first player agent.
    agent2 : Agent
        The second player agent.
    """
    agents = {1: agent1, -1: agent2}

    print(f"\nStarting game: {agent1} vs {agent2}")
    print("=" * 50)

    while not game.is_terminal():
        _, agentID = game.state
        current_agent = agents[agentID]

        try:
            action = current_agent.choose_action(game)
            if action is not None:
                game.next(action)
        except KeyboardInterrupt:
            print("\nGame interrupted by user.")
            return
        except Exception as e:
            print(f"Error: {e}")
            break

    print(f"\n{game}")
    print("=" * 50)


def main() -> None:
    """Main CLI function."""
    print("Welcome to the Games Collection!")
    print("=" * 40)

    while True:
        print("\nChoose a game:")
        print("1. Halving Game")
        print("2. Tic-Tac-Toe")
        print("3. Nim")
        print("4. Connect Four")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice (1-5): "))

            if choice == 5:
                print("Thanks for playing!")
                break
            elif choice == 1:
                print("\nHalving Game Rules:")
                print("- Start with a number")
                print("- Take turns to either subtract 1 or divide by 2")
                print("- Player who reaches 0 wins")

                starting_num = int(
                    input("Enter starting number (default 15): ") or "15"
                )
                game = HalvingGame(starting_num)

                agent1 = get_agent_choice(1)
                agent2 = get_agent_choice(-1)

                play_game(game, agent1, agent2)

            elif choice == 2:
                print("\nTic-Tac-Toe Rules:")
                print("- 3x3 grid")
                print("- First to get 3 in a row wins")
                print("- Player 1 is X, Player 2 is O")

                game = TicTacToeGame()

                agent1 = get_agent_choice(1)
                agent2 = get_agent_choice(-1)

                play_game(game, agent1, agent2)

            elif choice == 3:
                print("\nNim Rules:")
                print("- Multiple piles of objects")
                print("- Take turns removing any number from a single pile")
                print("- Player who takes the last object wins")

                print("Choose pile configuration:")
                print("1. Default (1, 3, 5, 7)")
                print("2. Custom")

                pile_choice = input("Enter choice (1-2, default 1): ") or "1"

                if pile_choice == "2":
                    pile_input = input(
                        "Enter pile sizes separated by commas (e.g., 2,4,6): "
                    )
                    try:
                        piles = [int(x.strip()) for x in pile_input.split(",")]
                        piles = [p for p in piles if p > 0]
                        if not piles:
                            print("Invalid input, using default piles")
                            piles = None
                    except ValueError:
                        print("Invalid input, using default piles")
                        piles = None
                    game = NimGame(piles)
                else:
                    game = NimGame()

                agent1 = get_agent_choice(1)
                agent2 = get_agent_choice(-1)

                play_game(game, agent1, agent2)

            elif choice == 4:
                print("\nConnect Four Rules:")
                print("- Choose board size (4x4 or 5x5)")
                print("- Drop pieces into columns")
                print("- First to get 4 in a row wins")
                print("- Player 1 is X, Player 2 is O")

                print("Choose board size:")
                print("1. 4x4 board")
                print("2. 5x5 board")

                board_choice = input("Enter choice (1-2, default 1): ") or "1"
                board_size = 4 if board_choice == "1" else 5

                game = ConnectFourGame(board_size)

                agent1 = get_agent_choice(1)
                agent2 = get_agent_choice(-1)

                play_game(game, agent1, agent2)

            else:
                print("Please enter 1, 2, 3, 4, or 5")

        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()
