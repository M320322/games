#!/usr/bin/env python3
"""
Build script to generate static HTML files for GitHub Pages deployment.
Since GitHub Pages doesn't support FastAPI, we'll create a static version
with client-side JavaScript that simulates the game logic.
"""

import os
import shutil
import json
from pathlib import Path

def create_dist_directory():
    """Create and clean the dist directory."""
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    return dist_dir

def copy_static_files(dist_dir):
    """Copy static CSS and JS files."""
    static_dir = dist_dir / "static"
    static_dir.mkdir()
    
    # Copy CSS
    shutil.copy("static/style.css", static_dir / "style.css")
    
    # Copy and modify JS for static site
    with open("static/script.js", "r") as f:
        js_content = f.read()
    
    with open(static_dir / "script.js", "w") as f:
        f.write(js_content)

def create_game_js(dist_dir):
    """Create JavaScript file with game logic for client-side execution."""
    js_content = """
// Client-side game implementations for static site

class HalvingGame {
    constructor(startingNumber = 15) {
        this.startingNumber = startingNumber;
        this.state = [startingNumber, 1]; // [number, player]
        this.gameHistory = [];
    }
    
    getActions() {
        const [number, player] = this.state;
        if (number === 0) return [];
        
        const actions = [];
        if (number > 0) actions.push('subtract');
        if (number % 2 === 0 && number > 0) actions.push('halve');
        return actions;
    }
    
    makeMove(action) {
        const [number, player] = this.state;
        let newNumber;
        
        if (action === 'subtract') {
            newNumber = number - 1;
        } else if (action === 'halve') {
            newNumber = Math.floor(number / 2);
        } else {
            throw new Error('Invalid action');
        }
        
        const nextPlayer = player === 1 ? 2 : 1;
        this.state = [newNumber, nextPlayer];
        this.gameHistory.push({action, player, number: newNumber});
        
        return this.getGameState();
    }
    
    isGameOver() {
        return this.state[0] === 0;
    }
    
    getWinner() {
        if (!this.isGameOver()) return null;
        const [number, currentPlayer] = this.state;
        return currentPlayer === 1 ? 2 : 1; // Previous player wins
    }
    
    getGameState() {
        return {
            number: this.state[0],
            current_player: this.state[1],
            is_game_over: this.isGameOver(),
            winner: this.getWinner(),
            valid_actions: this.getActions()
        };
    }
}

class TicTacToeGame {
    constructor() {
        this.board = Array(3).fill().map(() => Array(3).fill(0));
        this.currentPlayer = 1;
        this.gameHistory = [];
    }
    
    getActions() {
        if (this.isGameOver()) return [];
        
        const actions = [];
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                if (this.board[i][j] === 0) {
                    actions.push([i, j]);
                }
            }
        }
        return actions;
    }
    
    makeMove(row, col) {
        if (this.board[row][col] !== 0) {
            throw new Error('Position already occupied');
        }
        
        this.board[row][col] = this.currentPlayer;
        this.gameHistory.push({player: this.currentPlayer, row, col});
        this.currentPlayer = this.currentPlayer === 1 ? 2 : 1;
        
        return this.getGameState();
    }
    
    checkWinner() {
        // Check rows
        for (let row = 0; row < 3; row++) {
            if (this.board[row][0] === this.board[row][1] && 
                this.board[row][1] === this.board[row][2] && 
                this.board[row][0] !== 0) {
                return this.board[row][0];
            }
        }
        
        // Check columns
        for (let col = 0; col < 3; col++) {
            if (this.board[0][col] === this.board[1][col] && 
                this.board[1][col] === this.board[2][col] && 
                this.board[0][col] !== 0) {
                return this.board[0][col];
            }
        }
        
        // Check diagonals
        if (this.board[0][0] === this.board[1][1] && 
            this.board[1][1] === this.board[2][2] && 
            this.board[0][0] !== 0) {
            return this.board[0][0];
        }
        
        if (this.board[0][2] === this.board[1][1] && 
            this.board[1][1] === this.board[2][0] && 
            this.board[0][2] !== 0) {
            return this.board[0][2];
        }
        
        return null;
    }
    
    isGameOver() {
        return this.checkWinner() !== null || this.getActions().length === 0;
    }
    
    getGameState() {
        return {
            board: this.board.map(row => [...row]),
            current_player: this.currentPlayer,
            is_game_over: this.isGameOver(),
            winner: this.checkWinner(),
            valid_actions: this.getActions()
        };
    }
}

class RandomAgent {
    constructor(playerId) {
        this.playerId = playerId;
        this.name = 'Random AI';
    }
    
    chooseAction(game) {
        const actions = game.getActions();
        if (actions.length === 0) return null;
        return actions[Math.floor(Math.random() * actions.length)];
    }
}

class MinimaxAgent {
    constructor(playerId, maxDepth = 6) {
        this.playerId = playerId;
        this.name = 'Minimax AI';
        this.maxDepth = maxDepth;
    }
    
    chooseAction(game) {
        const actions = game.getActions();
        if (actions.length === 0) return null;
        if (actions.length === 1) return actions[0];
        
        let bestAction = null;
        let bestValue = -Infinity;
        
        for (const action of actions) {
            const gameCopy = this.copyGame(game);
            
            if (game instanceof HalvingGame) {
                gameCopy.makeMove(action);
            } else if (game instanceof TicTacToeGame) {
                gameCopy.makeMove(action[0], action[1]);
            }
            
            const value = this.minimax(gameCopy, 0, false, -Infinity, Infinity);
            
            if (value > bestValue) {
                bestValue = value;
                bestAction = action;
            }
        }
        
        return bestAction;
    }
    
    copyGame(game) {
        if (game instanceof HalvingGame) {
            const copy = new HalvingGame(game.startingNumber);
            copy.state = [...game.state];
            return copy;
        } else if (game instanceof TicTacToeGame) {
            const copy = new TicTacToeGame();
            copy.board = game.board.map(row => [...row]);
            copy.currentPlayer = game.currentPlayer;
            return copy;
        }
    }
    
    minimax(game, depth, maximizingPlayer, alpha, beta) {
        if (game.isGameOver() || depth >= this.maxDepth) {
            return this.evaluateGame(game);
        }
        
        const actions = game.getActions();
        
        if (maximizingPlayer) {
            let maxEval = -Infinity;
            for (const action of actions) {
                const gameCopy = this.copyGame(game);
                
                if (game instanceof HalvingGame) {
                    gameCopy.makeMove(action);
                } else if (game instanceof TicTacToeGame) {
                    gameCopy.makeMove(action[0], action[1]);
                }
                
                const eval = this.minimax(gameCopy, depth + 1, false, alpha, beta);
                maxEval = Math.max(maxEval, eval);
                alpha = Math.max(alpha, eval);
                
                if (beta <= alpha) break;
            }
            return maxEval;
        } else {
            let minEval = Infinity;
            for (const action of actions) {
                const gameCopy = this.copyGame(game);
                
                if (game instanceof HalvingGame) {
                    gameCopy.makeMove(action);
                } else if (game instanceof TicTacToeGame) {
                    gameCopy.makeMove(action[0], action[1]);
                }
                
                const eval = this.minimax(gameCopy, depth + 1, true, alpha, beta);
                minEval = Math.min(minEval, eval);
                beta = Math.min(beta, eval);
                
                if (beta <= alpha) break;
            }
            return minEval;
        }
    }
    
    evaluateGame(game) {
        if (!game.isGameOver()) return 0;
        
        if (game instanceof HalvingGame) {
            const winner = game.getWinner();
            return winner === this.playerId ? 1 : -1;
        } else if (game instanceof TicTacToeGame) {
            const winner = game.checkWinner();
            if (winner === null) return 0; // Draw
            return winner === this.playerId ? 1 : -1;
        }
        
        return 0;
    }
}

// Global variables for game management
window.GameClasses = { HalvingGame, TicTacToeGame };
window.AgentClasses = { RandomAgent, MinimaxAgent };
"""
    
    with open(dist_dir / "static" / "games.js", "w") as f:
        f.write(js_content)

def create_html_files(dist_dir):
    """Create static HTML files."""
    
    # Read templates and create static versions
    base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="static/style.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <h1><a href="index.html">Games Collection</a></h1>
            <ul class="nav-menu">
                <li><a href="index.html">Home</a></li>
                <li><a href="halving.html">Halving Game</a></li>
                <li><a href="tictactoe.html">Tic-Tac-Toe</a></li>
            </ul>
        </div>
    </nav>

    <main class="container">
        {content}
    </main>

    <script src="static/script.js"></script>
    <script src="static/games.js"></script>
    {scripts}
</body>
</html>"""
    
    # Index page
    index_content = """
    <div class="hero">
        <h1>Welcome to Games Collection</h1>
        <p>Choose a game to play against AI or human opponents</p>
    </div>

    <div class="games-grid">
        <div class="game-card">
            <h2>Halving Game</h2>
            <p>Start with a number and take turns to either subtract 1 or divide by 2. The player who reaches 0 wins!</p>
            <div class="game-rules">
                <h3>Rules:</h3>
                <ul>
                    <li>Players take turns</li>
                    <li>On your turn, either subtract 1 or divide by 2</li>
                    <li>You can only divide by 2 if the number is even</li>
                    <li>The player who makes the number 0 wins</li>
                </ul>
            </div>
            <a href="halving.html" class="btn btn-primary">Play Halving Game</a>
        </div>

        <div class="game-card">
            <h2>Tic-Tac-Toe</h2>
            <p>Classic 3x3 grid game. Get three in a row to win!</p>
            <div class="game-rules">
                <h3>Rules:</h3>
                <ul>
                    <li>Players take turns placing X and O</li>
                    <li>Player 1 is X, Player 2 is O</li>
                    <li>First to get 3 in a row wins</li>
                    <li>If the board is full with no winner, it's a draw</li>
                </ul>
            </div>
            <a href="tictactoe.html" class="btn btn-primary">Play Tic-Tac-Toe</a>
        </div>
    </div>
    """
    
    with open(dist_dir / "index.html", "w") as f:
        f.write(base_template.format(
            title="Home - Games Collection",
            content=index_content,
            scripts=""
        ))

def main():
    """Main build function."""
    print("Building static site for GitHub Pages...")
    
    # Create dist directory
    dist_dir = create_dist_directory()
    print(f"Created dist directory: {dist_dir}")
    
    # Copy static files
    copy_static_files(dist_dir)
    print("Copied static files")
    
    # Create game JavaScript
    create_game_js(dist_dir)
    print("Created game logic JavaScript")
    
    # Create HTML files
    create_html_files(dist_dir)
    print("Created HTML files")
    
    print("Build completed successfully!")

if __name__ == "__main__":
    main()
