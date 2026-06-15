from slot_engine import spin
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid

player_balance = 1000
bet_size = 10
allowed_bets = [10, 20, 40, 80, 120]

states = {}

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"name": "Leetcode1337"}
    )

@app.get("/spin")
async def spin_json():
    global player_balance
    if(player_balance >= bet_size):
        screen, winnings = spin()
        player_balance = (player_balance - bet_size) + winnings
        outcome = {
            "screen": screen,
            "winnings": winnings,
            "balance": player_balance
        }
        return outcome
    
@app.get("/state")
async def get_state():
    player_id = get_cookie()
    if player_id in states:
        return states[player_id]
    else:
        player_id = set_cookie()
        states[player_id]["balance"] = 1000
        states[player_id]["bet_size"] = 40
    
    return  states[player_id]

@app.get("/get_cookie")
async def get_cookie(request: Request):
    return request.cookies.get("player_id")

@app.get("/set_cookie")
async def set_cookie(response: Response):
    player_id = uuid.uuid4()
    response.set_cookie(key="player_id", value=player_id)
    return player_id
    
