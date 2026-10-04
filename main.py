from slot_machine import SlotMachine
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from player import Player, NotEnoughBalance, BetNotAllowed
from db import SessionLocal

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

def get_player(player_id, session):
    player = session.get(Player, player_id) if player_id else None
    return player

def get_or_create_player(player_id, session):
    player = get_player(player_id, session)
    if player is None:
        player = Player.make_player()
        session.add(player)
        
    return player

# when a GET request hits "/", FastAPI calls home(Request) and hands you the request object which is the home.html as a response
@app.get("/")
def home(request: Request):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        player = get_or_create_player(player_id, session)
        template_response = templates.TemplateResponse(
            request=request, name="home.html", context={"name": "Leetcode1337", "screen": player.screen}
        )
        template_response.set_cookie(key="player_id", value=player.id)
        session.commit()
        return template_response

# POST request hits "/spin", FastAPI calls spin_json(Request) and we check if the player already has a cookie set. This is the current way of identification. If they are present in the players table, we try a spin display the results to the user 
@app.post("/spin")
def spin_json(request: Request):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        player = get_player(player_id, session)
        
        if player is None:
            raise HTTPException(status_code=401, detail="No player session found")
        
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
            session.commit()
            return outcome
        except NotEnoughBalance:
            raise HTTPException(status_code=402, detail="not enough balance")
            

# Gets the player's cookie whether that's an actual cookie or None and calls get_or_create_player. After that it sets or re-sets the right cookie and returns the players balance and last win. 
@app.get("/state")
def get_state(request: Request, response: Response):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        player = get_or_create_player(player_id, session)
        response.set_cookie(key="player_id", value=player.id)
        session.commit()
        return {"balance": player.balance, "last_win": player.last_win}

# Resets the balance to the baseline
@app.post("/reset-balance")
def reset_balance(request: Request):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        player = get_player(player_id, session)

        if player is None:
            raise HTTPException(status_code=401, detail="No player session found")

        player.reset_balance()
        session.commit()
        return player.balance

# Player selects a bet amount 
@app.post("/bet")
def bet(bet_size: Bet, request: Request):
    with SessionLocal() as session:
        player_id = get_player_id(request)
        player = get_player(player_id, session)

        if player is None:
            raise HTTPException(status_code=401, detail="No player session found")
        try:
            player.change_bet_size(bet_size.bet_size)
            session.commit()
            return player.bet_size
        
        except BetNotAllowed:
            raise HTTPException(status_code=400, detail="Bet not allowed")

