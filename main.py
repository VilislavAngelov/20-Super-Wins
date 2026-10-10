from slot_machine import SlotMachine
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from player import NotEnoughBalance, BetNotAllowed
from db import SessionLocal
from services import CasinoService, PlayerNotFound

app = FastAPI()
machine = SlotMachine()

# serves the css/js/image files from the static/ folder.
app.mount("/static", StaticFiles(directory="static"), name="static")

# templating engine, in other words enables you to put dynamic values in the html ex. a python variable
templates = Jinja2Templates(directory="templates")

class Bet(BaseModel):
    bet_size: int

def get_player_id(request: Request):
    player_id = request.cookies.get("player_id")
    return player_id

# when a GET request hits "/", FastAPI calls home(Request) and hands you the request object which is the home.html as a response
@app.get("/")
def home(request: Request):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        casino = CasinoService(session, machine)
        player = casino.get_or_create_player(player_id)
        template_response = templates.TemplateResponse(
            request=request, name="home.html", context={"name": "Leetcode1337", "screen": player.screen}
        )
        template_response.set_cookie(key="player_id", value=player.id)

        return template_response

# POST request hits "/spin", FastAPI calls spin_json(Request) and we check if the player already has a cookie set. This is the current way of identification. If they are present in the players table, we try a spin display the results to the user 
@app.post("/spin")
def spin_json(request: Request):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        slot = CasinoService(session, machine)

        try:
            outcome = slot.spin(player_id)
        except PlayerNotFound:
            raise HTTPException(status_code=401, detail="No player session found")
        except NotEnoughBalance:
            raise HTTPException(status_code=402, detail="Not enough balance")
        return outcome
            

# Gets the player's cookie whether that's an actual cookie or None and calls get_or_create_player. After that it sets or re-sets the right cookie and returns the players balance and last win. 
@app.get("/state")
def get_state(request: Request, response: Response):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        casino = CasinoService(session, machine)
        player = casino.get_or_create_player(player_id)
        response.set_cookie(key="player_id", value=player.id)
        
        return {"balance": player.balance, "last_win": player.last_win}

# Resets the balance to the baseline
@app.post("/reset-balance")
def reset_balance(request: Request):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        casino = CasinoService(session, machine)

        try:
            balance = casino.player_reset_balance(player_id)
        except PlayerNotFound:
            raise HTTPException(status_code=401, detail="No player session found")

        return balance

# Player selects a bet amount 
@app.post("/bet")
def bet(bet_size: Bet, request: Request):
    with SessionLocal() as session:
        player_id = get_player_id(request)     
        casino = CasinoService(session, machine)

        try:
            player_bet = casino.player_change_bet(player_id, bet_size.bet_size)
        except PlayerNotFound:
            raise HTTPException(status_code=401, detail="No player session found")
        except BetNotAllowed:
            raise HTTPException(status_code=400, detail="Bet not allowed")

        return player_bet

@app.get("/history")
def latest_spins(request: Request):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        casino = CasinoService(session, machine)

        try:
            return casino.player_history(player_id)
        except PlayerNotFound:
            raise HTTPException(status_code=401, detail="No player session found")
        