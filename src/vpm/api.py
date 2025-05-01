# imports
from fastapi import FastAPI

# vpm imports
from database import create_db_and_tables, engine
from models import *
from main import *

app = FastAPI()

# overview endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to Virtual Property Manager"}

@app.get("/dashboard")
async def dashboard():
    return {"message": "User Dashboard"}
