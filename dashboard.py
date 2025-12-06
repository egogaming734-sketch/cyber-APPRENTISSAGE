#!/usr/bin/env python3
import time
import os
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1442275533697060874/Hd0j2d2Eo--ECxJCnuO2XVxga4KzMzWMDcU96JDWv6tv1fKGZTIDrOJewi8vNMEnC5nc"
LOG_FILE = "soc_events.log"

def log_event(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)

def send_discord(message):
    os.system(f'curl -s -H "Content-Type: application/json" -d \'{{"content": "{message}"}}\' {WEBHOOK_URL} > /dev/null')

def count_word(mot):
    try:
        with open("error_log.txt") as f:
            return sum(1 for line in f if mot in line)
    except:
        return 0

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

log_event("INFO", "J29 — MINI-SIEM démarre en mode silencieux")
print("\033[93m" + " " * 20 + "MINI-SIEM FRÉRO — J29 MODE SILENCIEUX" + "\033[0m")
time.sleep(2)

while True:
    clear()
    errors = count_word("ERROR")
    infos  = count_word("INFO")
    timestamp = datetime.now().strftime("%d/%m %H:%M:%S")

    bar_length = 30
    percent = min(errors * 10, 100)
    bar = "█" * (percent // 10 * 3) + "░" * (bar_length - percent // 10 * 3)

    print(f"\033[96m╔{'═' * 52}╗\033[0m")
    print(f"\033[96m║ MINI-SIEM FRÉRO                 {timestamp} ║\033[0m")
    print(f"\033[96m╠{'═' * 52}╣\033[0m")
    print(f"  INFO : {infos:>5}    │  ERROR : \033[91m{errors:>5}\033[0m")
    print(f"  DANGER : [{bar}] {percent:>3}%")
    print(f"\033[96m╚{'═' * 52}╝\033[0m")

    if errors >= 5:
        msg = f"ALERTE ROUGE → {errors} erreurs détectées !"
        log_event("CRITICAL", msg)
        send_discord(msg)
        print("\033[91m" + " "*12 + "ALERTE ROUGE LOGGÉE + DISCORD" + "\033[0m")
        os.system('echo -e "\a"')
    elif errors >= 3:
        log_event("WARNING", f"{errors} erreurs détectées")
        print("\033[93m" + " "*12 + "ALERTE ORANGE LOGGÉE" + "\033[0m")
    else:
        print(" "*12 + "\033[92mSystème stable\033[0m")

    time.sleep(5)
