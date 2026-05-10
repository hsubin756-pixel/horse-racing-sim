import sqlite3

conn = sqlite3.connect(r"C:\Users\bingi\Desktop\horse_project_v9\horse_racing.db")
cur = conn.cursor()
cur.execute("SELECT name, speed, stamina, sire_name FROM horses WHERE speed != 50 LIMIT 3")
rows = cur.fetchall()
print(rows)
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
        "pace": "normal"
    })
import random
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
            print(f"🔥 {h['name']} 라이벌 의식 발동!")
            rival_triggered.append(h["name"])  # ← 추가
        if h['pace']=="fast"and path==1:
            distance=distance+3
        if h['pace']=="fast"and path==3:
            distance=distance-3
        if h['pace']=="slow"and path==1:
            distance=distance-3
        if h['pace']=="slow"and path==3:
            distance=distance+3
        h["fatigue"] = h["fatigue"] + (10 - h["stamina"])
        h["total"] = h["total"] + distance
        print(f"[{path}구간] {h['name']} {'─' * distance}({distance})")
for horse in horses:
    if horse['fatigue']>=25:
        horse['injured']=True
    else:
        horse['injured']=False
result = sorted(horses, key=lambda h: h["total"], reverse=True)
print("===== 결과 =====")
for i,horse in enumerate(result):
    if i==0:
        medal="🥇"
    elif i==1:
        medal = "🥈"
    else:
        medal = "🥉"
    injury = "⚠ 부상" if horse["injured"] else ""
    print(f"{medal} {i+1}위: {horse['name']} (총 거리: {horse['total']}){injury}{horse['fatigue']}")
winner = result[0]["name"]
for name in rival_triggered:
    if name != winner:
        cur.execute("UPDATE horses SET rival_name = ? WHERE name = ?", (winner, name))
        conn.commit()
        print(f"🏇 {name} 의 라이벌로 {winner} 가 등록됐습니다")
cur.execute("UPDATE horses SET rival_name = NULL WHERE name = rival_name")
conn.commit()

