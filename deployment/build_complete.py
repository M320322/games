#!/usr/bin/env python3
"""
Complete static site builder with all HTML pages.
"""

import os
import shutil
from pathlib import Path

def create_halving_html(dist_dir):
    """Create halving game HTML."""
    halving_content = """
    <div class="game-page">
        <h1>Halving Game</h1>
        
        <div class="game-setup" id="gameSetup">
            <h2>Game Setup</h2>
            <div class="form-group">
                <label for="startingNumber">Starting Number:</label>
                <input type="number" id="startingNumber" value="15" min="1" max="100">
            </div>
            
            <div class="form-group">
                <label for="player1Type">Player 1:</label>
                <select id="player1Type">
                    <option value="human">Human</option>
                    <option value="random">Random AI</option>
                    <option value="minimax">Minimax AI</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="player2Type">Player 2:</label>
                <select id="player2Type">
                    <option value="random" selected>Random AI</option>
                    <option value="human">Human</option>
                    <option value="minimax">Minimax AI</option>
                </select>
            </div>
            
            <button type="button" class="btn btn-primary" onclick="startHalvingGame()">Start Game</button>
        </div>

        <div class="game-area" id="gameArea" style="display: none;">
            <div class="game-state">
                <h2>Current Number: <span id="currentNumber"></span></h2>
                <p id="currentPlayer"></p>
                <p id="gameStatus"></p>
            </div>
            
            <div class="game-actions" id="gameActions">
                <h3>Choose your action:</h3>
                <div class="action-buttons">
                    <button class="btn btn-action" onclick="makeHalvingMove('subtract')">Subtract 1</button>
                    <button class="btn btn-action" onclick="makeHalvingMove('halve')">Divide by 2</button>
                </div>
            </div>
            
            <button class="btn btn-secondary" onclick="resetHalvingGame()">New Game</button>
        </div>
    </div>
    """
    
    halving_scripts = """
    <script>
    let currentHalvingGame = null;
    let halvingAgents = {};
    
    function startHalvingGame() {
        const startingNumber = parseInt(document.getElementById('startingNumber').value);
        const player1Type = document.getElementById('player1Type').value;
        const player2Type = document.getElementById('player2Type').value;
        
        currentHalvingGame = new GameClasses.HalvingGame(startingNumber);
        
        halvingAgents = {
            1: player1Type === 'human' ? null : 
                player1Type === 'random' ? new AgentClasses.RandomAgent(1) :
                new AgentClasses.MinimaxAgent(1),
            2: player2Type === 'human' ? null :
                player2Type === 'random' ? new AgentClasses.RandomAgent(2) :
                new AgentClasses.MinimaxAgent(2)
        };
        
        document.getElementById('gameSetup').style.display = 'none';
        document.getElementById('gameArea').style.display = 'block';
        
        updateHalvingDisplay();
    }
    
    function makeHalvingMove(action) {
        if (!currentHalvingGame || currentHalvingGame.isGameOver()) return;
        
        try {
            currentHalvingGame.makeMove(action);
            updateHalvingDisplay();
            
            // Auto-play AI moves
            setTimeout(playAIMove, 500);
        } catch (error) {
            alert(error.message);
        }
    }
    
    function playAIMove() {
        if (!currentHalvingGame || currentHalvingGame.isGameOver()) return;
        
        const currentAgent = halvingAgents[currentHalvingGame.state[1]];
        if (currentAgent) {
            const action = currentAgent.chooseAction(currentHalvingGame);
            if (action) {
                currentHalvingGame.makeMove(action);
                updateHalvingDisplay();
                
                // Continue with next AI move if needed
                setTimeout(playAIMove, 1000);
            }
        }
    }
    
    function updateHalvingDisplay() {
        const gameState = currentHalvingGame.getGameState();
        
        document.getElementById('currentNumber').textContent = gameState.number;
        
        if (gameState.is_game_over) {
            document.getElementById('currentPlayer').textContent = '';
            document.getElementById('gameStatus').textContent = `Game Over! Player ${gameState.winner} wins!`;
            document.getElementById('gameActions').style.display = 'none';
        } else {
            document.getElementById('currentPlayer').textContent = `Player ${gameState.current_player}'s turn`;
            document.getElementById('gameStatus').textContent = '';
            
            // Show/hide action buttons
            const subtractBtn = document.querySelector('[onclick="makeHalvingMove(\\'subtract\\')"]');
            const halveBtn = document.querySelector('[onclick="makeHalvingMove(\\'halve\\')"]');
            
            subtractBtn.style.display = gameState.valid_actions.includes('subtract') ? 'inline-block' : 'none';
            halveBtn.style.display = gameState.valid_actions.includes('halve') ? 'inline-block' : 'none';
            
            // Hide actions if it's AI turn
            const currentAgent = halvingAgents[gameState.current_player];
            if (currentAgent) {
                document.getElementById('gameActions').style.display = 'none';
                setTimeout(playAIMove, 1000);
            } else {
                document.getElementById('gameActions').style.display = 'block';
            }
        }
    }
    
    function resetHalvingGame() {
        currentHalvingGame = null;
        halvingAgents = {};
        document.getElementById('gameSetup').style.display = 'block';
        document.getElementById('gameArea').style.display = 'none';
    }
    </script>
    """
    
    base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Halving Game - Games Collection</title>
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
</html>""".format(content=halving_content, scripts=halving_scripts)
    
    with open(dist_dir / "halving.html", "w") as f:
        f.write(base_template)

def create_tictactoe_html(dist_dir):
    """Create tic-tac-toe game HTML."""
    tictactoe_content = """
    <div class="game-page">
        <h1>Tic-Tac-Toe</h1>
        
        <div class="game-setup" id="gameSetup">
            <h2>Game Setup</h2>
            <div class="form-group">
                <label for="player1Type">Player 1 (X):</label>
                <select id="player1Type">
                    <option value="human" selected>Human</option>
                    <option value="random">Random AI</option>
                    <option value="minimax">Minimax AI</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="player2Type">Player 2 (O):</label>
                <select id="player2Type">
                    <option value="random" selected>Random AI</option>
                    <option value="human">Human</option>
                    <option value="minimax">Minimax AI</option>
                </select>
            </div>
            
            <button type="button" class="btn btn-primary" onclick="startTicTacToeGame()">Start Game</button>
        </div>

        <div class="game-area" id="gameArea" style="display: none;">
            <div class="game-state">
                <p id="currentPlayer"></p>
                <p id="gameStatus"></p>
            </div>
            
            <div class="tictactoe-board" id="board">
                <!-- Board will be generated by JavaScript -->
            </div>
            
            <button class="btn btn-secondary" onclick="resetTicTacToeGame()">New Game</button>
        </div>
    </div>
    """
    
    tictactoe_scripts = """
    <script>
    let currentTicTacToeGame = null;
    let tictactoeAgents = {};
    
    function startTicTacToeGame() {
        const player1Type = document.getElementById('player1Type').value;
        const player2Type = document.getElementById('player2Type').value;
        
        currentTicTacToeGame = new GameClasses.TicTacToeGame();
        
        tictactoeAgents = {
            1: player1Type === 'human' ? null : 
                player1Type === 'random' ? new AgentClasses.RandomAgent(1) :
                new AgentClasses.MinimaxAgent(1),
            2: player2Type === 'human' ? null :
                player2Type === 'random' ? new AgentClasses.RandomAgent(2) :
                new AgentClasses.MinimaxAgent(2)
        };
        
        document.getElementById('gameSetup').style.display = 'none';
        document.getElementById('gameArea').style.display = 'block';
        
        updateTicTacToeDisplay();
    }
    
    function makeTicTacToeMove(row, col) {
        if (!currentTicTacToeGame || currentTicTacToeGame.isGameOver()) return;
        
        try {
            currentTicTacToeGame.makeMove(row, col);
            updateTicTacToeDisplay();
            
            // Auto-play AI moves
            setTimeout(playTicTacToeAIMove, 500);
        } catch (error) {
            alert(error.message);
        }
    }
    
    function playTicTacToeAIMove() {
        if (!currentTicTacToeGame || currentTicTacToeGame.isGameOver()) return;
        
        const currentAgent = tictactoeAgents[currentTicTacToeGame.currentPlayer];
        if (currentAgent) {
            const action = currentAgent.chooseAction(currentTicTacToeGame);
            if (action) {
                currentTicTacToeGame.makeMove(action[0], action[1]);
                updateTicTacToeDisplay();
                
                // Continue with next AI move if needed
                setTimeout(playTicTacToeAIMove, 1000);
            }
        }
    }
    
    function updateTicTacToeDisplay() {
        const gameState = currentTicTacToeGame.getGameState();
        
        // Update board display
        const board = document.getElementById('board');
        board.innerHTML = '';
        
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                const cell = document.createElement('div');
                cell.className = 'board-cell';
                
                const cellValue = gameState.board[i][j];
                if (cellValue === 1) {
                    cell.textContent = 'X';
                    cell.classList.add('player-x');
                } else if (cellValue === 2) {
                    cell.textContent = 'O';
                    cell.classList.add('player-o');
                } else {
                    cell.textContent = '';
                    if (!gameState.is_game_over) {
                        cell.onclick = () => makeTicTacToeMove(i, j);
                        cell.classList.add('clickable');
                    }
                }
                
                board.appendChild(cell);
            }
        }
        
        // Update game status
        if (gameState.is_game_over) {
            document.getElementById('currentPlayer').textContent = '';
            if (gameState.winner) {
                const symbol = gameState.winner === 1 ? 'X' : 'O';
                document.getElementById('gameStatus').textContent = `Game Over! Player ${gameState.winner} (${symbol}) wins!`;
            } else {
                document.getElementById('gameStatus').textContent = 'Game Over! It\\'s a draw!';
            }
        } else {
            const symbol = gameState.current_player === 1 ? 'X' : 'O';
            document.getElementById('currentPlayer').textContent = `Player ${gameState.current_player} (${symbol})'s turn`;
            document.getElementById('gameStatus').textContent = '';
            
            // Check if it's AI turn
            const currentAgent = tictactoeAgents[gameState.current_player];
            if (currentAgent) {
                setTimeout(playTicTacToeAIMove, 1000);
            }
        }
    }
    
    function resetTicTacToeGame() {
        currentTicTacToeGame = null;
        tictactoeAgents = {};
        document.getElementById('gameSetup').style.display = 'block';
        document.getElementById('gameArea').style.display = 'none';
    }
    </script>
    """
    
    base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tic-Tac-Toe - Games Collection</title>
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
</html>""".format(content=tictactoe_content, scripts=tictactoe_scripts)
    
    with open(dist_dir / "tictactoe.html", "w") as f:
        f.write(base_template)

# Update the main build script
def update_build_script():
    """Update the build script to include all HTML files."""
    with open("deployment/build_static.py", "a") as f:
        f.write("""
def create_complete_html_files(dist_dir):
    \"\"\"Create all static HTML files.\"\"\"
    create_halving_html(dist_dir)
    create_tictactoe_html(dist_dir)

# Add these imports at the top
from deployment.build_complete import create_halving_html, create_tictactoe_html

# Update main function to call create_complete_html_files
""")

if __name__ == "__main__":
    # This file contains the helper functions for build_static.py
    pass
