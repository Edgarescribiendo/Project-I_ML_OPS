import fastapi
import pandas as pd
from fastapi import FastAPI
import uvicorn
from functions import *

app = FastAPI()

#data_steam = pd.read_csv('EDA/data_merged.csv')

#http://127.0.0.1:8000/ Ruta madre del puerto

@app.get("/")
def root():
    return {'message':'hey!, Listen!!'}

@app.get("/developer/{desarrollador}") 
async def desarrollador(desarrollador:str):     
    try:         
        result_1 = developer(desarrollador)         
        return result_1     
    except Exception as e:         
        return {"error": str(e)}

@app.get("/userdata/{user_id}")
async def user(user_id: str):
    try:
        result_2 = userdata(user_id)
        return result_2
    except Exception as e:
        return {"error": str(e)}


@app.get("/best_developer_year/{year}")
async def Best_developer_year(year: str):
    try:
        year_number = int(year)  # Convertir el año a un entero
        result_3 = best_developer_year(year_number)
        return result_3
    except Exception as e:
        return {"error": str(e)} 

#uvicorn main:app --reload



