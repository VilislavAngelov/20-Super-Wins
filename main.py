from slot_engine import spin
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/spin")
async def spin_json():
    return spin()