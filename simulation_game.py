"""
Game simulation for statistical analysis.

This module simulates multiple games between different agent types
and generates statistics including winner, steps to win, and computation time.
"""

import os
import shutil
import time
import random
import logging
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import List, Dict, Any
from games import HalvingGame, TicTacToeGame
from agents import RandomAgent, MinimaxAgent, Agent
from games.base_game import Game

random.seed(42)  # For reproducibility


class GameSimulator:
    """
    Simulator for running multiple games and collecting statistics.
    """

    def __init__(self, output_dir: str = "results", max_workers: int = 4):
        self.results: List[Dict[str, Any]] = []
        self.output_dir = output_dir
        self.max_workers = max_workers
        self.log_file = os.path.join(self.output_dir, "simulation.log")
        self.csv_file = os.path.join(self.output_dir, "results.csv")
        self.results_lock = Lock()

        self._setup_output_directory()
        self._setup_logging()

    def _setup_output_directory(self) -> None:
        """Create output directory and remove existing files."""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

        os.makedirs(self.output_dir, exist_ok=True)

    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger(__name__)

    def simulate_game(
        self, game: Game, agent1: Agent, agent2: Agent, initial_number: int = None
    ) -> Dict[str, Any]:
        """
        Simulate a single game between two agents and collect statistics.

        Parameters
        ----------
        game : Game
            The game instance to play.
        agent1 : Agent
            The first player agent.
        agent2 : Agent
            The second player agent.
        initial_number : int, optional
            The initial number for halving games.

        Returns
        -------
        Dict[str, Any]
            Dictionary containing game statistics.
        """
        agents = {1: agent1, -1: agent2}
        player1_computation_time = 0.0
        player2_computation_time = 0.0
        total_moves = 0

        while not game.is_terminal():
            _, current_player_id = game.state
            current_agent = agents[current_player_id]

            start_time = time.time()
            try:
                action = current_agent.choose_action(game)
                if action is not None:
                    game.next(action)
                    total_moves += 1
            except Exception as e:
                self.logger.error(f"Error in game simulation: {e}")
                break
            end_time = time.time()

            if current_player_id == 1:
                player1_computation_time += end_time - start_time
            else:
                player2_computation_time += end_time - start_time

        winner = game.get_winner()

        result = {
            "player1_agent": agent1.name,
            "player2_agent": agent2.name,
            "winner": winner if winner is not None else 0,
            "total_moves": total_moves,
            "player1_computation_time": player1_computation_time,
            "player2_computation_time": player2_computation_time,
        }

        if initial_number is not None:
            result["initial_number"] = initial_number

        return result

    def _run_single_game_simulation(
        self,
        game_class,
        game_args: tuple,
        agent1_class,
        agent2_class,
        game_name: str,
        match_number: int,
        randomize_initial: bool = False,
        initial_range: tuple = (10, 20),
    ) -> Dict[str, Any]:
        """
        Run a single game simulation. This method is designed to be thread-safe.

        Parameters
        ----------
        game_class : class
            The game class to instantiate.
        game_args : tuple
            Arguments to pass to the game constructor.
        agent1_class : class
            The first agent class.
        agent2_class : class
            The second agent class.
        game_name : str
            Name of the game for identification.
        match_number : int
            The match number for this game.
        randomize_initial : bool
            Whether to randomize the initial number (for halving games).
        initial_range : tuple
            Range for random initial numbers (min, max).

        Returns
        -------
        Dict[str, Any]
            Dictionary containing game statistics.
        """
        thread_random = random.Random()

        if randomize_initial and game_class == HalvingGame:
            initial_number = thread_random.randint(*initial_range)
            game = game_class(initial_number)
        else:
            game = game_class(*game_args)
            initial_number = (
                game_args[0] if game_args and game_class == HalvingGame else None
            )

        agent1_seed = thread_random.randint(1, 1000000)
        agent2_seed = thread_random.randint(1, 1000000)

        agent1 = agent1_class(1, random_seed=agent1_seed)
        agent2 = agent2_class(-1, random_seed=agent2_seed)

        result = self.simulate_game(game, agent1, agent2, initial_number)
        result["game_type"] = game_name
        result["match_number"] = match_number

        return result

    def run_simulation_batch(
        self,
        game_class,
        game_args: tuple,
        agent1_class,
        agent2_class,
        num_games: int,
        game_name: str,
        randomize_initial: bool = False,
        initial_range: tuple = (10, 20),
    ) -> None:
        """
        Run a batch of simulations for a specific game and agent combination using multithreading.

        Parameters
        ----------
        game_class : class
            The game class to instantiate.
        game_args : tuple
            Arguments to pass to the game constructor.
        agent1_class : class
            The first agent class.
        agent2_class : class
            The second agent class.
        num_games : int
            Number of games to simulate.
        game_name : str
            Name of the game for identification.
        randomize_initial : bool
            Whether to randomize the initial number (for halving games).
        initial_range : tuple
            Range for random initial numbers (min, max).
        """
        self.logger.info(
            f"Running {num_games} {game_name} games: {agent1_class.__name__} vs {agent2_class.__name__} (using {self.max_workers} threads)"
        )

        completed_games = 0
        batch_results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_game = {
                executor.submit(
                    self._run_single_game_simulation,
                    game_class,
                    game_args,
                    agent1_class,
                    agent2_class,
                    game_name,
                    i + 1,
                    randomize_initial,
                    initial_range,
                ): i + 1
                for i in range(num_games)
            }

            for future in as_completed(future_to_game):
                try:
                    result = future.result()
                    batch_results.append(result)
                    completed_games += 1

                    if completed_games % 25 == 0:
                        self.logger.info(
                            f"  Completed {completed_games}/{num_games} games"
                        )

                except Exception as e:
                    match_number = future_to_game[future]
                    self.logger.error(f"Error in game {match_number}: {e}")

        with self.results_lock:
            self.results.extend(batch_results)

        self.logger.info(
            f"  Batch completed: {completed_games}/{num_games} games successful"
        )

    def run_all_simulations(self) -> None:
        """
        Run all specified game simulations.
        """
        self.logger.info("Starting game simulations...")
        self.logger.info("=" * 60)

        n: int = 200  # Number of games to simulate for each pair

        self.logger.info("--- HALVING GAME SIMULATIONS ---")

        # Random vs Minimax with randomized initial numbers
        self.run_simulation_batch(
            HalvingGame,
            (),
            RandomAgent,
            MinimaxAgent,
            n,
            "Halving Game",
            randomize_initial=True,
            initial_range=(10, 20),
        )

        # Minimax vs Minimax with randomized initial numbers
        self.run_simulation_batch(
            HalvingGame,
            (),
            MinimaxAgent,
            MinimaxAgent,
            n,
            "Halving Game",
            randomize_initial=True,
            initial_range=(10, 20),
        )

        # Minimax vs Random with randomized initial numbers
        self.run_simulation_batch(
            HalvingGame,
            (),
            MinimaxAgent,
            RandomAgent,
            n,
            "Halving Game",
            randomize_initial=True,
            initial_range=(10, 20),
        )

        # Random vs Random with randomized initial numbers
        self.run_simulation_batch(
            HalvingGame,
            (),
            RandomAgent,
            RandomAgent,
            n,
            "Halving Game",
            randomize_initial=True,
            initial_range=(10, 20),
        )

        self.logger.info("--- TIC-TAC-TOE SIMULATIONS ---")

        # Random vs Minimax
        self.run_simulation_batch(
            TicTacToeGame, (), RandomAgent, MinimaxAgent, n, "Tic-Tac-Toe"
        )

        # Minimax vs Minimax
        self.run_simulation_batch(
            TicTacToeGame, (), MinimaxAgent, MinimaxAgent, n, "Tic-Tac-Toe"
        )

        # Minimax vs Random
        self.run_simulation_batch(
            TicTacToeGame, (), MinimaxAgent, RandomAgent, n, "Tic-Tac-Toe"
        )

        # Random vs Random
        self.run_simulation_batch(
            TicTacToeGame, (), RandomAgent, RandomAgent, n, "Tic-Tac-Toe"
        )

        self.logger.info("All simulations completed!")
        self.logger.info(f"Total games simulated: {len(self.results)}")

    def save_results_to_csv(self) -> None:
        """
        Save simulation results to a CSV file in the output directory.
        """
        if not self.results:
            self.logger.warning("No results to save. Run simulations first.")
            return

        df = pd.DataFrame(self.results)

        base_columns = [
            "game_type",
            "match_number",
            "player1_agent",
            "player2_agent",
            "winner",
            "total_moves",
            "player1_computation_time",
            "player2_computation_time",
        ]

        # Add initial_number column for halving games
        if "initial_number" in df.columns:
            column_order = base_columns[:2] + ["initial_number"] + base_columns[2:]
        else:
            column_order = base_columns

        df = df[column_order]

        df.to_csv(self.csv_file, index=False)
        self.logger.info(f"Results saved to {self.csv_file}")

        self.print_summary_statistics(df)

    def print_summary_statistics(self, df: pd.DataFrame) -> None:
        """
        Print summary statistics of the simulation results.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing simulation results.
        """
        self.logger.info("\n" + "=" * 60)
        self.logger.info("SIMULATION SUMMARY STATISTICS")
        self.logger.info("=" * 60)

        for game_type in df["game_type"].unique():
            game_df = df[df["game_type"] == game_type]
            self.logger.info(f"\n--- {game_type.upper()} ---")

            combinations = game_df.groupby(["player1_agent", "player2_agent"])

            for (agent1, agent2), group in combinations:
                self.logger.info(f"\n{agent1} vs {agent2} ({len(group)} games):")

                # Winner statistics
                winner_counts = group["winner"].value_counts()
                if 1 in winner_counts:
                    self.logger.info(
                        f"  Player 1 ({agent1}) wins: {winner_counts[1]} ({winner_counts[1] / len(group) * 100:.1f}%)"
                    )
                if -1 in winner_counts:
                    self.logger.info(
                        f"  Player 2 ({agent2}) wins: {winner_counts[-1]} ({winner_counts[-1] / len(group) * 100:.1f}%)"
                    )
                if 0 in winner_counts:
                    self.logger.info(
                        f"  Draws: {winner_counts[0]} ({winner_counts[0] / len(group) * 100:.1f}%)"
                    )

                # Moves statistics
                self.logger.info(
                    f"  Average moves per game: {group['total_moves'].mean():.2f}"
                )
                self.logger.info(
                    f"  Min/Max moves: {group['total_moves'].min()}/{group['total_moves'].max()}"
                )

                # Time statistics
                self.logger.info(
                    f"  Avg computation time - Player 1: {group['player1_computation_time'].mean():.4f}s"
                )
                self.logger.info(
                    f"  Avg computation time - Player 2: {group['player2_computation_time'].mean():.4f}s"
                )

                # Initial number statistics for halving games
                if "initial_number" in group.columns:
                    self.logger.info(
                        f"  Initial number range: {group['initial_number'].min()}-{group['initial_number'].max()}"
                    )
                    self.logger.info(
                        f"  Average initial number: {group['initial_number'].mean():.1f}"
                    )


def main():
    """
    Main function to run the game simulations.
    """
    import multiprocessing

    max_workers = max(multiprocessing.cpu_count(), 8)

    simulator = GameSimulator(max_workers=max_workers)

    simulator.logger.info(f"Starting simulations with {max_workers} worker threads")

    start_time = time.time()
    simulator.run_all_simulations()
    end_time = time.time()

    simulator.logger.info(
        f"\nTotal simulation time: {end_time - start_time:.2f} seconds"
    )

    simulator.save_results_to_csv()


if __name__ == "__main__":
    main()
