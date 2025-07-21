# Games Collection

A collection of classic games with AI agents.

## 🎮 Games

### Halving Game
- Start with a positive integer
- Players take turns to either subtract 1 or divide by 2 (integer division)
- Player who reduces the number to 0 wins
- Strategic thinking required to force optimal positions

### Tic-Tac-Toe
- Classic 3x3 grid game
- Players alternate placing X and O
- First to get three in a row wins
- Supports draws when board is full

### Nim
- Multiple piles of objects (stones, matches, etc.)
- Players take turns removing any number of objects from a single pile
- The player who takes the last object wins

### Connect Four
- Choose between 4x4 or 5x5 grid
- Players take turns dropping pieces into columns
- Pieces fall to the lowest available position in a column
- First to get 4 in a row (horizontal, vertical, or diagonal) wins

## 🤖 Agents

### Human Agent
- Takes input from command line or web interface

### Random Agent
- Chooses moves randomly from valid actions

### Minimax Agent
- Uses minimax algorithm for perfect strategy

## 🚀 Quick Start

### Command Line Interface

```bash
# Install dependencies
pip install -e .

# Run CLI version
python ./cli_game.py
```

### Web Interface (Local)

```bash
# Start FastAPI server
python ./main.py

# Visit http://localhost:8000
```

### GitHub Pages (Static)

Web interface is deployed to GitHub Pages at https://M320322.github.io/games/

## 📁 Project Structure

```
games/
├── games/                  # Game implementations
│   ├── __init__.py
│   ├── base_game.py        # Abstract base game class
│   ├── halving_game.py     # Halving game implementation
│   ├── tictactoe_game.py   # Tic-tac-toe implementation
│   ├── nim_game.py         # Nim game implementation
│   └── connectfour_game.py # Connect Four implementation
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py       # Abstract base agent class
│   ├── human_agent.py      # Human player interface
│   ├── random_agent.py     # Random move agent
│   └── minimax_agent.py    # Minimax algorithm agent
├── deployment/             # Deployment and build scripts
│   ├── build_static.py
│   └── build_complete.py
├── static/                 # Static web assets
│   ├── style.css
│   └── script.js
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── halving.html
│   ├── tictactoe.html
│   ├── nim.html
│   └── connectfour.html
├── .github/workflows/      # GitHub Actions for deployment
│   └── deploy.yml
├── .gitignore              # Git ignore file
├── .python-version
├── cli_game.py             # Command line interface
├── main.py                 # FastAPI web application
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```