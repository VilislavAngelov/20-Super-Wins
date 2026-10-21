from fastapi import FastAPI, Request, Response, Depends, Cookie, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from player import Player

router = APIRouter()
templates = Jinja2Templates(directory="templates")

PlayerId = Annotated[str | None, Cookie()]

def get_or_create_player(self, player_id):
    player = self.session.get(Player, player_id) if player_id else None
    if player is None:
        player = Player.make_player()
        self.session.add(player)
        self.session.commit()
    
    return player

@router.get("/roulette")
def home(request: Request):
    template_response = templates.TemplateResponse(
        request=request, name="roulette.html", context={"name": "Leetcode1337"}
    )

    return template_response