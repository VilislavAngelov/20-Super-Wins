from slot_machine import SlotMachine
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from player import Player, NotEnoughBalance, BetNotAllowed

players = {}
app = FastAPI()
machine = SlotMachine()

# serves the css/js/image files from the static/ folder.
app.mount("/static", StaticFiles(directory="static"), name="static")

# templating engine, in other words enables you to put dynamic values in the html ex. a python variable
templates = Jinja2Templates(directory="templates")

class Bet(BaseModel):
    bet_size: int

def get_or_create_player(player_id):

    if player_id in players:
        return players[player_id]
    else:
        player = Player.make_player()
        players[player.id] = player
        
    return player

# when a GET request hits "/", FastAPI calls home(Request) and hands you the request object which is the home.html as a response
@app.get("/")
async def home(request: Request):
    player_id = request.cookies.get("player_id")
    player = get_or_create_player(player_id)
    template_response = templates.TemplateResponse(
        request=request, name="home.html", context={"name": "Leetcode1337", "screen": player.screen}
    )
    template_response.set_cookie(key="player_id", value=player.id)
    return template_response

# POST request hits "/spin", FastAPI calls spin_json(Request) and we check if the player already has a cookie set. This is the current way of identification. If they are present in the dict players, we try a spin display the results to the user 
@app.post("/spin")
async def spin_json(request: Request):
    player_id = request.cookies.get("player_id")
    if player_id in players:
        player = players[player_id]
        try: 
            player.pay_bet()
            spin_balance = player.balance
            result = machine.spin()
            player.collect_wins(result.winnings)
            player.screen = result.screen
            outcome = {
                "screen": result.screen,
                "winnings": result.winnings,
                "balance": player.balance,
                "last_win": player.last_win,
                "spin_balance": spin_balance,
                "wins": result.wins
            }
            return outcome
        except NotEnoughBalance:
            raise HTTPException(status_code=402, detail="not enough balance")
        
    else:
        raise HTTPException(status_code=401, detail="No player session found")

# Gets the player's cookie whether that's an actual cookie or None and calls get_or_create_player. After that it sets or re-sets the right cookie and returns the players balance and last win. 
@app.get("/state")
async def get_state(request: Request, response: Response):
    player_id = request.cookies.get("player_id")
    player = get_or_create_player(player_id)
    response.set_cookie(key="player_id", value=player.id)
    return {"balance": player.balance, "last_win": player.last_win}

# Resets the balance to the baseline
@app.post("/reset-balance")
async def reset_balance(request: Request):
    player_id = request.cookies.get("player_id")
    if player_id in players:
        players[player_id].reset_balance()
    
        return  players[player_id].balance
    else:
        raise HTTPException(status_code=401, detail="No player session found")

# Player selects a bet amount 
@app.post("/bet")
async def bet(bet_size: Bet, request: Request):
    player_id = request.cookies.get("player_id")
    if player_id in players:
        try:
            player = players[player_id]
            player.change_bet_size(bet_size.bet_size)
            return player.bet_size
        except BetNotAllowed:
            raise HTTPException(status_code=400, detail="Bet not allowed")
    else:
        raise HTTPException(status_code=401, detail="No player session found")