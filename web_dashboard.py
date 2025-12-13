#!/usr/bin/env python3
from flask import Flask, render_template_string
import time
from datetime import datetime
import os

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
            return f.read().strip().split("\n")[-10:][::-1]
    except:
        return ["Aucun historique"]

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>MINI-SIEM FRÉRO — J31</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: monospace; background: #000; color: #0f0; text-align: center; transition: background 0.5s; }
        .bar { background: #333; width: 50%; margin: 20px auto; height: 30px; }
        .fill { background: #f00; height: 100%; transition: width 1s; }
        .alert { animation: blink 1s infinite; }
        @keyframes blink { 0% { color: #f00; } 50% { color: #fff; } 100% { color: #f00; } }
        .flash { animation: flash 1s infinite; }
        @keyframes flash { 0% { background: #300; } 50% { background: #f00; } 100% { background: #300; } }
    </style>
    <script>
        function playAlarm() {
            var audio = new Audio('https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3');
            audio.loop = true;
            audio.play();
        }
        {% if alert %}
            window.onload = playAlarm;
        {% endif %}
    </script>
</head>
<body class="{% if alert %}flash{% endif %}">
    <h1 class="{% if alert %}alert{% endif %}">MINI-SIEM LIVE — {{ timestamp }}</h1>
    <h2>INFO : {{ infos }} | ERROR : <span style="color:red">{{ errors }}</span></h2>
    <div class="bar"><div class="fill" style="width: {{ percent }}%"></div></div>
    <h3>DANGER : {{ percent }}%</h3>
    <hr>
    <h3>Dernières alertes :</h3>
    {% for line in history %}
        <p>{{ line }}</p>
    {% endfor %}
    <br>
    <a href="/test" style="font-size: {% if alert %}50px{% else %}20px{% endif %}; color: {% if alert %}red{% else %}yellow{% endif %}">
        [ TEST ALERTE ]
    </a>
</body>
</html>
'''

@app.route("/")
def dashboard():
    errors = count_word("ERROR")
    alert = errors >= 5
    percent = min(errors * 10, 100)
    return render_template_string(HTML, 
        timestamp=datetime.now().strftime("%d/%m %H:%M:%S"),
        infos=count_word("INFO"), errors=errors, percent=percent,
        history=get_history(), alert=alert
    )

@app.route("/test")
def test():
    os.system(f'curl -s -H "Content-Type: application/json" -d \'{{"content": "🚨 TEST ALERTE J31 — SIRÈNE + CLIGNOTEMENT !!"}}\' {WEBHOOK_URL}')
    return "<h1 style='color:red'>TEST ENVOYÉ + SIRÈNE ACTIVÉE !</h1><a href='/'>Retour</a>"

if __name__ == "__main__":
    print("J31 → Dashboard avec clignotement + sirène navigateur → http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
