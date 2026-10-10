from slot_machine import SlotMachine
from fastapi import FastAPI, Request, Response, Depends, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from player import PlayerError
from db import get_session
from services import CasinoService
from typing import Annotated

app = FastAPI()
machine = SlotMachine()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class Bet(BaseModel):
    bet_size: int

def get_casino(session=Depends(get_session)):
    return CasinoService(session, machine)

Casino = Annotated[CasinoService, Depends(get_casino)]
PlayerId = Annotated[str | None, Cookie()]

@app.exception_handler(PlayerError)
def player_error(request: Request, exc: PlayerError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.get("/")
def home(casino: Casino, request: Request, player_id: PlayerId = None):
    player = casino.get_or_create_player(player_id)
    template_response = templates.TemplateResponse(
        request=request, name="home.html", context={"name": "Leetcode1337", "screen": player.screen}
    )
    template_response.set_cookie(key="player_id", value=player.id)

    return template_response

@app.post("/spin")
def spin_json(casino: Casino, player_id: PlayerId = None):

    return casino.spin(player_id)
    
@app.get("/state")
def get_state(casino: Casino, response: Response, player_id: PlayerId = None):
    player = casino.get_or_create_player(player_id)
    response.set_cookie(key="player_id", value=player.id)
    
    return {"balance": player.balance, "last_win": player.last_win}

@app.post("/reset-balance")
def reset_balance(casino: Casino, player_id: PlayerId = None):
    balance = casino.player_reset_balance(player_id)

    return balance

@app.post("/bet")
def bet(casino: Casino, bet_size: Bet, player_id: PlayerId = None):
    player_bet = casino.player_change_bet(player_id, bet_size.bet_size)

    return player_bet

@app.get("/history")
def latest_spins(casino: Casino, player_id: PlayerId = None):
    
    return casino.player_history(player_id)
    