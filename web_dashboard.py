#!/usr/bin/env python3
from flask import Flask, render_template_string, send_file, request
import time
from datetime import datetime, timedelta
import sqlite3
import os
import csv
from io import StringIO

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1442275533697060874/Hd0j2d2Eo--ECxJCnuO2XVxga4KzMzWMDcU96JDWv6tv1fKGZTIDrOJewi8vNMEnC5nc"
DB_FILE = "soc.db"

# Création table (déjà fait)
conn = sqlite3.connect(DB_FILE)
conn.execute('''
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    level TEXT,
    message TEXT
)
''')
conn.commit()
conn.close()

def log_event(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_FILE)
    conn.execute("INSERT INTO alerts (timestamp, level, message) VALUES (?, ?, ?)", (timestamp, level, message))
    conn.commit()
    conn.close()

def send_discord(message):
    os.system(f'curl -s -H "Content-Type: application/json" -d \'{{"content": "{message}"}}\' {WEBHOOK_URL} > /dev/null')

def count_word(mot):
    try:
        with open("error_log.txt") as f:
            return sum(1 for line in f if mot in line)
    except:
        return 0

def get_stats():
    conn = sqlite3.connect(DB_FILE)
    today = datetime.now().strftime("%Y-%m-%d")
    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
    total = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    today_count = conn.execute("SELECT COUNT(*) FROM alerts WHERE level='CRITICAL' AND timestamp LIKE ?", (f"{today}%",)).fetchone()[0]
    week_count = conn.execute("SELECT COUNT(*) FROM alerts WHERE level='CRITICAL' AND timestamp >= ?", (f"{week_start} 00:00:00",)).fetchone()[0]
    conn.close()
    return today_count, week_count, total

def get_week_graph():
    conn = sqlite3.connect(DB_FILE)
    days = []
    counts = []
    for i in range(6, -1, -1):
        day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        count = conn.execute("SELECT COUNT(*) FROM alerts WHERE level='CRITICAL' AND timestamp LIKE ?", (f"{day}%",)).fetchone()[0]
        days.append(day[5:])
        counts.append(count)
    conn.close()
    max_count = max(counts) if counts else 1
    graph = ""
    for i in range(max_count, 0, -1):
        line = ""
        for c in counts:
            line += "█" if c >= i else "░"
            line += "  "
        graph += line + "\n"
    graph += " ".join([d[3:] for d in days])
    return graph

def get_average():
    conn = sqlite3.connect(DB_FILE)
    total = conn.execute("SELECT COUNT(*) FROM alerts WHERE level='CRITICAL'").fetchone()[0]
    first = conn.execute("SELECT MIN(timestamp) FROM alerts").fetchone()[0]
    conn.close()
    if not first:
        return 0
    days = (datetime.now() - datetime.strptime(first, "%Y-%m-%d %H:%M:%S")).days + 1
    return round(total / days, 1)

def get_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT timestamp, level, message FROM alerts ORDER BY id DESC LIMIT 10")
    history = [f"[{row[0]}] [{row[1]}] {row[2]}" for row in cursor]
    conn.close()
    return history[::-1]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>MINI-SIEM FRÉRO — J36</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: monospace; transition: all 0.5s; }
        .dark { background: #000; color: #0f0; }
        .light { background: #fff; color: #000; }
        .bar { background: #333; width: 50%; margin: 20px auto; height: 30px; }
        .fill { background: #f00; height: 100%; transition: width 1s; }
        .light .bar { background: #ddd; }
        .light .fill { background: #c00; }
    </style>
</head>
<body class="{{ theme }}">
    <h1>MINI-SIEM LIVE — {{ timestamp }}</h1>
    <h2>INFO : {{ infos }} | ERROR : <span style="color:red">{{ errors }}</span></h2>
    <div class="bar"><div class="fill" style="width: {{ percent }}%"></div></div>
    <h3>DANGER : {{ percent }}%</h3>
    <hr>
    <h3>STATS AVANCÉES :</h3>
    <p>Alertes CRITICAL aujourd'hui : <span style="color:red">{{ today }}</span></p>
    <p>Alertes CRITICAL cette semaine : <span style="color:red">{{ week }}</span></p>
    <p>Total alertes depuis le début : <span style="color:yellow">{{ total }}</span></p>
    <p>Moyenne erreurs/jour : <span style="color:cyan">{{ average }}</span></p>
    <hr>
    <h3>Graphique semaine :</h3>
    <pre>{{ graph }}</pre>
    <hr>
    <a href="/export">[ EXPORTER EN CSV ]</a>
    <br><br>
    <a href="/change-theme" style="font-size: 25px; color: cyan">[ CHANGER THÈME ]</a>
    <hr>
    <h3>Dernières alertes :</h3>
    {% for line in history %}
        <p>{{ line }}</p>
    {% endfor %}
    <br>
    <a href="/test">[ TEST ALERTE ]</a>
</body>
</html>
'''

@app.route("/")
def dashboard():
    errors = count_word("ERROR")
    infos = count_word("INFO")
    percent = min(errors * 10, 100)
    today, week, total = get_stats()
    average = get_average()
    graph = get_week_graph()
    alert = errors >= 5
    theme = request.cookies.get('theme', 'dark')
    if alert:
        log_event("CRITICAL", f"ALERTE ROUGE → {errors} erreurs détectées !")
        send_discord(f"**ALERTE ROUGE** → {errors} erreurs (J36 Thème)")
    response = render_template_string(HTML, 
        timestamp=datetime.now().strftime("%d/%m %H:%M:%S"),
        infos=infos, errors=errors, percent=percent,
        today=today, week=week, total=total, average=average,
        graph=graph,
        history=get_history(), alert=alert, theme=theme
    )
    return response

@app.route("/test")
def test():
    log_event("TEST", "Test depuis J36")
    send_discord("**TEST** depuis J36")
    return "<h1>TEST ENVOYÉ + LOGGÉ EN DB !</h1><a href='/'>Retour</a>"

@app.route("/export")
def export():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT timestamp, level, message FROM alerts ORDER BY id DESC")
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Timestamp", "Level", "Message"])
    writer.writerows(cursor)
    output.seek(0)
    conn.close()
    return send_file(output, mimetype="text/csv", as_attachment=True, download_name="soc_alerts.csv")

@app.route("/change-theme")
def change_theme():
    theme = request.cookies.get('theme', 'dark')
    new_theme = 'light' if theme == 'dark' else 'dark'
    response = app.make_response("<h1>Thème changé ! <a href='/'>Retour</a></h1>")
    response.set_cookie('theme', new_theme, max_age=60*60*24*365)  # 1 an
    return response

if __name__ == "__main__":
    print("J36 → Dashboard avec thème sombre/clair → http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
