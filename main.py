# imports from various libraries. 
from slot_engine import spin, symbols_multiplier
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid
from pydantic import BaseModel

allowed_bets = (10, 20, 40, 80, 120)
states = {}
app = FastAPI()
slot_symbols = list(symbols_multiplier.keys())

start_screen = [
            ["🍉", "🍉", "🍉"],   # reel 0
            ["🍇", "🍇", "🍇"],   # reel 1
            ["🍋", "🍋", "🍋"],   # reel 2
            ["🍊", "🍊", "🍊"],   # reel 3
            ["🍒", "🍒", "🍒"],
        ]

# serves the css/js/image files from the static/ folder.
app.mount("/static", StaticFiles(directory="static"), name="static")

# templating engine, in other words enables you to put dynamic values in the html ex. a python variable
templates = Jinja2Templates(directory="templates")

class Bet(BaseModel):
    bet_size: int

def get_or_create_player(player_id):

    if player_id in states:
        return player_id, states[player_id]
    else:
        player_id = str(uuid.uuid4())
        states[player_id] = {}
        states[player_id]["balance"] = 1000
        states[player_id]["bet_size"] = 40
        states[player_id]["last_win"] = 0
        states[player_id]["screen"] = start_screen
        
    return player_id, states[player_id]

# when a GET request hits "/", FastAPI calls home(Request) and hands you the request object which is the home.html as a response
@app.get("/")
async def home(request: Request):
    player_id = request.cookies.get("player_id")
    player_id, player_state = get_or_create_player(player_id)
    template_response = templates.TemplateResponse(
        request=request, name="home.html", context={"name": "Leetcode1337", "screen": player_state["screen"]}
    )
    template_response.set_cookie(key="player_id", value=player_id)
    return template_response

# GET request hits "/spin", FastAPI calls spin_json(Request) and we check if the player already has a cookie set. This is the current way of identification. If they are present in the dict states, we assing them their balance , last bet_size and last win. then we call spin and display the results to the user 
#TODO add the last screen they have seen to the state
@app.post("/spin")
async def spin_json(request: Request):
    player_id = request.cookies.get("player_id")
    if player_id in states:
        player = states[player_id]
        if player["balance"] < player["bet_size"]:
            raise HTTPException(status_code=402, detail="not enough balance")
        else:
            screen, winnings, wins = spin()
            player["spin_balance"] = player["balance"] - player["bet_size"]
            player["balance"] = (player["balance"] - player["bet_size"]) + winnings
            if winnings > 0:
                player["last_win"] = winnings
            player["screen"] = screen
            outcome = {
                    "screen": screen,
                    "winnings": winnings,
                    "balance": player["balance"],
                    "last_win": player["last_win"],
                    "spin_balance": player["spin_balance"],
                    "wins": wins
            }
        return outcome
    else:
        raise HTTPException(status_code=401, detail="No player session found")

# Checks if player the player cookie is in the existing dict and if not it creates a new user id , assigns the baseline balance and bet size and saves the uid as a cookie and returns the cookie 
@app.get("/state")
async def get_state(request: Request, response: Response):
    player_id = request.cookies.get("player_id")
    player_id, player_state = get_or_create_player(player_id)
    response.set_cookie(key="player_id", value=player_id)
    return  player_state

# Resets the balance to the baseline
@app.post("/reset-balance")
async def reset_balance(request: Request):
    player_id = request.cookies.get("player_id")
    if player_id in states:
        states[player_id]["balance"] = 1000
    
        return  states[player_id]["balance"]
    else:
        raise HTTPException(status_code=401, detail="No player session found")

# Player selects a bet amount 
@app.post("/bet")
async def bet(bet_size: Bet, request: Request):
    player_id = request.cookies.get("player_id")
    if player_id in states:
        if bet_size.bet_size in allowed_bets:
            states[player_id]["bet_size"] = bet_size.bet_size
            return bet_size.bet_size
        else:
            raise HTTPException(status_code=400, detail="Bet not allowed")
    else:
        raise HTTPException(status_code=401, detail="No player session found")