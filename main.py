from slot_engine import spin
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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
    return spin()
