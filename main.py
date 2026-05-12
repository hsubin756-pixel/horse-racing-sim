from engine import load_horses, run_race
from fastapi import FastAPI
import sqlite3
import random

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "경마 서버 시작"}

@app.get("/race")
def race():
    horses=load_horses()
    result=run_race(horses)
    return result
@app.get("/auction")
def auction():
    conn = sqlite3.connect(r"C:\Users\bingi\Desktop\horse_project_v9\horse_racing.db")
    cur = conn.cursor()
    cur.execute("SELECT name, speed, stamina, sire_name FROM horses WHERE speed != 50 LIMIT 3")
    rows = cur.fetchall()
    horses = []
    for row in rows:
        name,speed,stamina,sire_name=row[0],row[1]//10,row[2]//10,row[3]
        cur.execute("SELECT speed, stamina FROM horses WHERE name = ?", (sire_name,))
        sire = cur.fetchone()
        if sire:
            if sire[0]>=80:
                speed=speed+3
            if sire[1]>=80:
                stamina=stamina+3
        horses.append({
            "name": name,
            "speed": speed,
            "stamina": stamina,   
        })
    for horse in horses:
        horse["price"]=(horse["speed"]+horse["stamina"])*100
    return {"auction":horses}
    