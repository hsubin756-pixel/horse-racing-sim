import csv
import random
import sqlite3

conn = sqlite3.connect(r"C:\Users\bingi\Desktop\horse_project_v9\horse_racing.db")
cur = conn.cursor()
cur.execute("SELECT name, speed, stamina, sire_name FROM horses WHERE speed != 50 LIMIT 10")
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
    horses.append({"name": name, "speed": speed,"base_speed": speed, "stamina": stamina, "pace": "normal"})

results = []

for i in range(100):
    for horse in horses:
        horse["total"] = 0
        horse["fatigue"] = 0
        horse["speed"] = horse["base_speed"] + random.randint(-1, 1)

    for path in range(1, 4):
        if path == 3:
            lead = max(h["total"] for h in horses)
        for h in horses:
            speed = h["speed"]
            distance = speed + random.randint(1, 3) - h["fatigue"] // 3
            if path == 3 and (lead - h["total"]) <= 5:
                distance = distance + 2
            h["fatigue"] = h["fatigue"] + (10 - h["stamina"])
            h["total"] = h["total"] + distance

    result = sorted(horses, key=lambda h: h["total"], reverse=True)
    for rank, horse in enumerate(result):
        results.append([horse["name"], horse["speed"], horse["stamina"], rank + 1])

with open("race_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "speed", "stamina", "rank"])
    for row in results:
        writer.writerow(row)

print("완료! 총", len(results), "개 데이터")
