"""
FastAPI web application for playing games through a web interface.
"""

from typing import Any

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from games import HalvingGame, TicTacToeGame, NimGame, ConnectFourGame
from agents import RandomAgent, MinimaxAgent, Agent

app = FastAPI(title="Games Collection", description="Play Halving Game and Tic-Tac-Toe")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Global game state (in a real app, you'd use a database or session storage)
game_sessions: dict[int, dict] = {}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """
    Home page with game selection.

    Parameters
    ----------
    request : Request
        The FastAPI request object.

    Returns
    -------
    HTMLResponse
        The rendered home page template.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/halving", response_class=HTMLResponse)
async def halving_game_page(request: Request) -> HTMLResponse:
    """
    Halving game page.

    Parameters
    ----------
    request : Request
        The FastAPI request object.

    Returns
    -------
    HTMLResponse
        The rendered halving game template.
    """
    return templates.TemplateResponse("halving.html", {"request": request})


@app.get("/tictactoe", response_class=HTMLResponse)
async def tictactoe_game_page(request: Request) -> HTMLResponse:
    """
    Tic-tac-toe game page.

    Parameters
    ----------
    request : Request
        The FastAPI request object.

    Returns
    -------
    HTMLResponse
        The rendered tic-tac-toe template.
    """
    return templates.TemplateResponse("tictactoe.html", {"request": request})


@app.get("/nim", response_class=HTMLResponse)
async def nim_game_page(request: Request) -> HTMLResponse:
    """
    Nim game page.

    Parameters
    ----------
    request : Request
        The FastAPI request object.

    Returns
    -------
    HTMLResponse
        The rendered nim template.
    """
    return templates.TemplateResponse("nim.html", {"request": request})


@app.get("/connectfour", response_class=HTMLResponse)
async def connectfour_game_page(request: Request) -> HTMLResponse:
    """
    Connect Four game page.

    Parameters
    ----------
    request : Request
        The FastAPI request object.

    Returns
    -------
    HTMLResponse
        The rendered Connect Four template.
    """
    return templates.TemplateResponse("connectfour.html", {"request": request})


@app.post("/api/halving/new")
async def new_halving_game(
    starting_number: int = Form(15),
    player1_type: str = Form("human"),
    player2_type: str = Form("random"),
) -> dict[str, Any]:
    """
    Start a new halving game.

    Parameters
    ----------
    starting_number : int, default=15
        The starting number for the game.
    player1_type : str, default="human"
        The type of agent for player 1.
    player2_type : str, default="random"
        The type of agent for player 2.

    Returns
    -------
    dict[str, Any]
        Dictionary containing session ID and initial game state.
    """
    game = HalvingGame(starting_number)

    # Create session ID (simple counter for demo)
    session_id = len(game_sessions) + 1

    game_sessions[session_id] = {
        "game": game,
        "player1_type": player1_type,
        "player2_type": player2_type,
        "agents": {
            1: _create_agent(player1_type, 1),
            -1: _create_agent(player2_type, -1),
        },
    }

    # Auto-play AI moves if the current player is an AI
    _auto_play_ai_moves(session_id)

    return {"session_id": session_id, "game_state": game.get_state_display()}


@app.post("/api/tictactoe/new")
async def new_tictactoe_game(
    player1_type: str = Form("human"), player2_type: str = Form("random")
) -> dict[str, Any]:
    """
    Start a new tic-tac-toe game.

    Parameters
    ----------
    player1_type : str, default="human"
        The type of agent for player 1.
    player2_type : str, default="random"
        The type of agent for player 2.

    Returns
    -------
    dict[str, Any]
        Dictionary containing session ID and initial game state.
    """
    game = TicTacToeGame()

    # Create session ID (simple counter for demo)
    session_id = len(game_sessions) + 1

    game_sessions[session_id] = {
        "game": game,
        "player1_type": player1_type,
        "player2_type": player2_type,
        "agents": {
            1: _create_agent(player1_type, 1),
            -1: _create_agent(player2_type, -1),
        },
    }

    # Auto-play AI moves if the current player is an AI
    _auto_play_ai_moves(session_id)

    return {"session_id": session_id, "game_state": game.get_state_display()}


@app.post("/api/nim/new")
async def new_nim_game(
    piles: str = Form("1,3,5,7"),
    player1_type: str = Form("human"),
    player2_type: str = Form("random"),
) -> dict[str, Any]:
    """
    Start a new nim game.

    Parameters
    ----------
    piles : str, default="1,3,5,7"
        Comma-separated pile sizes.
    player1_type : str, default="human"
        The type of agent for player 1.
    player2_type : str, default="random"
        The type of agent for player 2.

    Returns
    -------
    dict[str, Any]
        Dictionary containing session ID and initial game state.
    """
    try:
        pile_sizes = [int(x.strip()) for x in piles.split(",") if x.strip()]
        pile_sizes = [p for p in pile_sizes if p > 0]  # Filter positive numbers
        if not pile_sizes:
            pile_sizes = None  # Use default
    except ValueError:
        pile_sizes = None  # Use default

    game = NimGame(pile_sizes)

    # Create session ID (simple counter for demo)
    session_id = len(game_sessions) + 1

    game_sessions[session_id] = {
        "game": game,
        "player1_type": player1_type,
        "player2_type": player2_type,
        "agents": {
            1: _create_agent(player1_type, 1),
            -1: _create_agent(player2_type, -1),
        },
    }

    # Auto-play AI moves if the current player is an AI
    _auto_play_ai_moves(session_id)

    return {"session_id": session_id, "game_state": game.get_state_display()}


@app.post("/api/connectfour/new")
async def new_connectfour_game(
    board_size: int = Form(4),
    player1_type: str = Form("human"),
    player2_type: str = Form("random"),
) -> dict[str, Any]:
    """
    Start a new Connect Four game.

    Parameters
    ----------
    board_size : int, default=4
        The board size (4 or 5).
    player1_type : str, default="human"
        The type of agent for player 1.
    player2_type : str, default="random"
        The type of agent for player 2.

    Returns
    -------
    dict[str, Any]
        Dictionary containing session ID and initial game state.
    """
    if board_size not in [4, 5]:
        board_size = 4  # Default to 4 if invalid

    game = ConnectFourGame(board_size)

    # Create session ID (simple counter for demo)
    session_id = len(game_sessions) + 1

    game_sessions[session_id] = {
        "game": game,
        "player1_type": player1_type,
        "player2_type": player2_type,
        "agents": {
            1: _create_agent(player1_type, 1),
            -1: _create_agent(player2_type, -1),
        },
    }

    # Auto-play AI moves if the current player is an AI
    _auto_play_ai_moves(session_id)

    return {"session_id": session_id, "game_state": game.get_state_display()}


@app.post("/api/game/{session_id}/move")
async def make_move(session_id: int, action: str = Form(...)) -> dict[str, Any]:
    """
    Make a move in the game.

    Parameters
    ----------
    session_id : int
        The game session ID.
    action : str
        The action to take (format depends on game type).

    Returns
    -------
    dict[str, Any]
        Dictionary containing success status and updated game state or error message.
    """
    if session_id not in game_sessions:
        return {"error": "Game session not found"}

    session = game_sessions[session_id]
    game = session["game"]

    if game.is_game_over():
        return {"error": "Game is already over"}

    try:
        # Parse action based on game type
        if isinstance(game, HalvingGame):
            parsed_action = action
        elif isinstance(game, TicTacToeGame):
            # Action should be in format "row,col"
            row, col = map(int, action.split(","))
            parsed_action = (row, col)
        elif isinstance(game, NimGame):
            # Action should be in format "pile_index,objects_to_remove"
            pile_idx, objects_to_remove = map(int, action.split(","))
            parsed_action = (pile_idx, objects_to_remove)
        elif isinstance(game, ConnectFourGame):
            # Action should be a column number
            parsed_action = int(action)

        game.move(parsed_action)

        # Auto-play AI moves
        _auto_play_ai_moves(session_id)

        return {"success": True, "game_state": game.get_state_display()}

    except Exception as e:
        return {"error": str(e)}


@app.get("/api/game/{session_id}/state")
async def get_game_state(session_id: int) -> dict[str, Any]:
    """
    Get current game state.

    Parameters
    ----------
    session_id : int
        The game session ID.

    Returns
    -------
    dict[str, Any]
        Dictionary containing current game state or error message.
    """
    if session_id not in game_sessions:
        return {"error": "Game session not found"}

    game = game_sessions[session_id]["game"]
    return game.get_state_display()


def _create_agent(agent_type: str, player_id: int) -> Agent | None:
    """
    Create an agent based on type.

    Parameters
    ----------
    agent_type : str
        The type of agent to create ("random", "minimax", or "human").
    player_id : int
        The player ID for the agent.

    Returns
    -------
    Agent or None
        The created agent instance, or None for human players.
    """
    if agent_type == "random":
        return RandomAgent(player_id)
    elif agent_type == "minimax":
        return MinimaxAgent(player_id)
    else:
        return None


def _auto_play_ai_moves(session_id: int) -> None:
    """
    Auto-play AI moves until it's a human player's turn or game is over.

    Parameters
    ----------
    session_id : int
        The game session ID.
    """
    if session_id not in game_sessions:
        return

    session = game_sessions[session_id]
    game = session["game"]

    # Auto-play AI moves
    while not game.is_game_over():
        current_agent = session["agents"][game.current_player]
        if isinstance(current_agent, (RandomAgent, MinimaxAgent)):
            ai_action = current_agent.choose_action(game)
            if ai_action:
                game.move(ai_action)
            else:
                break
        else:
            break  # Wait for human input


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
