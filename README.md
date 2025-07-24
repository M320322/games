# Games Collection

A collection of classic games with AI agents.

## 🎮 Games

### Halving Game
- Start with a positive integer
- Players take turns to either subtract 1 or divide by 2 (integer division)
- Player who reduces the number to 0 wins

### Tic-Tac-Toe
- Classic 3x3 grid game
- Players alternate placing X and O
- First to get three in a row wins

### Nim
- Multiple piles of objects (stones, matches, etc.)
- Players take turns removing any number of objects from a single pile
- The player who takes the last object wins

### Connect Four
- Choose between 4x4 or 5x5 grid
- Players take turns dropping pieces into columns
- First to get 4 in a row (horizontal, vertical, or diagonal) wins

## 🤖 Agents

### Human Agent
- Takes input from command line

### Random Agent
- Chooses moves randomly from valid actions

### Minimax Agent
- Uses minimax algorithm for optimal strategy

## 🚀 Usage

### Command Line Interface

```bash
# Play games
python cli_game.py
```

### Simulation and Analysis

```bash
# Run game simulations for statistical analysis
python simulation_game.py
```

The simulation runs multiple games between different agent combinations and saves results to [/results/results.csv](./results/results.csv) with statistics including:
- Winner information
- Game duration (total moves)
- Computation time per player
- Summary statistics logged to [/results/simulation.log](./results/simulation.log)

## 📁 Project Structure

```
games/
├── games/                  # Game implementations
│   ├── base_game.py        # Abstract base game class
│   ├── halving_game.py     # Halving game implementation
│   ├── tictactoe_game.py   # Tic-tac-toe implementation
│   ├── nim_game.py         # Nim game implementation
│   └── connectfour_game.py # Connect Four implementation
├── agents/                 # Agent implementations
│   ├── base_agent.py       # Abstract base agent class
│   ├── human_agent.py      # Human player interface
│   ├── random_agent.py     # Random move agent
│   └── minimax_agent.py    # Minimax algorithm agent
├── cli_game.py             # Interactive command line interface
├── simulation_game.py      # Automated game simulation and analysis
└── pyproject.toml          # Project configuration
```

## 🐛 Bug Reports

If you encounter any bugs or issues while using this games collection, please report them to: [menlu@seas.upenn.edu](mailto:menlu@seas.upenn.edu)
