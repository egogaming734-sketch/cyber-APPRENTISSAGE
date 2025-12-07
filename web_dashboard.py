#!/usr/bin/env python3
from flask import Flask, render_template_string
import time
from datetime import datetime

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1442275533697060874/Hd0j2d2Eo--ECxJCnuO2XVxga4KzMzWMDcU96JDWv6tv1fKGZTIDrOJewi8vNMEnC5nc"

def count_word(mot):
    try:
        with open("error_log.txt") as f:
            return sum(1 for line in f if mot in line)
    except:
        return 0

def get_history():
    try:
        with open("soc_events.log") as f:
            return f.read().strip().split("\n")[-10:][::-1]  # 10 dernières lignes
    except:
        return ["Aucun historique"]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>MINI-SIEM FRÉRO — J30</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: monospace; background: #000; color: #0f0; text-align: center; }
        .bar { background: #333; width: 50%; margin: 20px auto; height: 30px; }
        .fill { background: #f00; height: 100%; }
    </style>
</head>
<body>
    <h1>🔥 MINI-SIEM LIVE — {{ timestamp }}</h1>
    <h2>INFO : {{ infos }} | ERROR : <span style="color:red">{{ errors }}</span></h2>
    <div class="bar"><div class="fill" style="width: {{ percent }}%"></div></div>
    <h3>DANGER : {{ percent }}%</h3>
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
    return render_template_string(HTML, 
        timestamp=datetime.now().strftime("%d/%m %H:%M:%S"),
        infos=infos, errors=errors, percent=percent,
        history=get_history()
    )

@app.route("/test")
def test():
    from os import system
    system(f'curl -s -H "Content-Type: application/json" -d \'{{"content": "🚨 TEST ALERTE DEPUIS LA WEB UI !!"}}\' {WEBHOOK_URL}')
    return "<h1>ALERTE TEST ENVOYÉE !</h1><a href='/'>Retour</a>"

if __name__ == "__main__":
    print("J30 → Web UI dispo sur http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
