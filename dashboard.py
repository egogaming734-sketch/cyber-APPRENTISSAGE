#!/usr/bin/env python3
import time
import os
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1442275533697060874/Hd0j2d2Eo--ECxJCnuO2XVxga4KzMzWMDcU96JDWv6tv1fKGZTIDrOJewi8vNMEnC5nc"
ALERT_LOG = "alert_history.log"

def send_discord(msg):
    os.system(f'curl -s -H "Content-Type: application/json" -d \'{{"content": "{msg}"}}\' {WEBHOOK_URL} > /dev/null')

def log_alert(errors):
    now = datetime.now().strftime("%H:%M")
    with open(ALERT_LOG, "a") as f:
        f.write(f"[{now}] ALERTE ROUGE → {errors} erreurs\n")

def count_today_alerts():
    try:
        today = datetime.now().strftime("%d/%m")
        count = 0
        with open(ALERT_LOG) as f:
            for line in f:
                if today in line.split("[")[1][:5]:
                    count += 1
        return count
    except:
        return 0

def count_word(mot):
    try:
        with open("error_log.txt") as f:
            return sum(1 for line in f if mot in line)
    except:
        return 0

def clear(): os.system('clear' if os.name == 'posix' else 'cls')

print("\033[93m" + " " * 20 + "MINI-SIEM FRÉRO — J28 🔥" + "\033[0m")
time.sleep(2)

while True:
    clear()
    errors = count_word("ERROR")
    infos  = count_word("INFO")
    today_alerts = count_today_alerts()
    timestamp = datetime.now().strftime("%d/%m %H:%M:%S")

    bar_length = 30
    percent = min(errors * 10, 100)
    bar = "█" * (percent//10*3) + "░" * (bar_length - percent//10*3)

    print(f"\033[96m╔{'═' * 52}╗\033[0m")
    print(f"\033[96m║ MINI-SIEM FRÉRO                 {timestamp} ║\033[0m")
    print(f"\033[96m╠{'═' * 52}╣\033[0m")
    print(f"  INFO : {infos:>5}    │  ERROR : \033[91m{errors:>5}\033[0m")
    print(f"  DANGER : [{bar}] {percent:>3}%")
    print(f"\033[96m╠{'═' * 52}╣\033[0m")
    print(f"  ALERTES AUJOURD'HUI : \033[93m{today_alerts:>3}\033[0m")
    if today_alerts > 0:
        print(f"  DERNIÈRE : {open(ALERT_LOG).readlines()[-1].strip() if os.path.exists(ALERT_LOG) else 'Aucune'}")
    print(f"\033[96m╚{'═' * 52}╝\033[0m")

    if errors >= 5 and (time.time() % 30 < 5):  # alerte max toutes les 30s
        msg = f"ALERTE ROUGE → {errors} erreurs détectées !"
        send_discord(msg)
        log_alert(errors)
        print("\033[91m" + " "*12 + "ALERTE ROUGE ENVOYÉE + HISTORIQUE SAUVÉ" + "\033[0m")
        os.system('echo -e "\a"')

    time.sleep(5)
