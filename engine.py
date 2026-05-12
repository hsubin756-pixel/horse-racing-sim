import sqlite3
import random

def load_horses():
    conn = sqlite3.connect(r"C:\Users\bingi\Desktop\horse_project_v9\horse_racing.db")
    cur = conn.cursor()
    cur.execute("SELECT name, speed, stamina, sire_name FROM horses WHERE speed != 50 LIMIT 3")
    rows = cur.fetchall()
    
    horses = []
    for row in rows:
        name, speed, stamina, sire_name = row[0], row[1]//10, row[2]//10, row[3]
        cur.execute("SELECT speed, stamina FROM horses WHERE name = ?", (sire_name,))
        sire = cur.fetchone()
        if sire:
            if sire[0] >= 80:
                speed = speed + 3
            if sire[1] >= 80:
                stamina = stamina + 3
        horses.append({"name": name, "speed": speed, "stamina": stamina, "pace": "normal"})
    return horses
def run_race(horses):
    rival_triggered = []
    for horse in horses:
        horse["total"] = 0
        horse["fatigue"] = 0

    for path in range(1, 4):
        if path == 3:
            lead = max(h["total"] for h in horses)
        for h in horses:
            speed = h["speed"]
            distance = speed + random.randint(1, 3) - h["fatigue"] // 3
            if path == 3 and (lead - h["total"]) <= 5:
                distance = distance + 2
                rival_triggered.append(h["name"])
            h["fatigue"] = h["fatigue"] + (10 - h["stamina"])
            h["total"] = h["total"] + distance

    for horse in horses:
        horse["injured"] = horse["fatigue"] >= 25

    result = sorted(horses, key=lambda h: h["total"], reverse=True)
    return {"result": result}
