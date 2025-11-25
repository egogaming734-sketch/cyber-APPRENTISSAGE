#!/usr/bin/env python3
import requests
import time
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1442275533697060874/Hd0j2d2Eo--ECxJCnuO2XVxga4KzMzWMDcU96JDWv6tv1fKGZTIDrOJewi8vNMEnC5nc"

def send_discord(message):
    data = {"content": message}
    requests.post(WEBHOOK_URL, json=data)

def count_word(fichier, mot):
    c = 0
    try:
        with open(fichier, "r") as file:
            for line in file:
                if mot in line:
                    c += 1
    except:
        pass
    return c

# Couleurs terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Son d'alarme (marche sur WSL + Windows)
def beep():
    print('\a', end='')  # BIP dans le terminal
    os.system('powershell -c "(New-Object Media.SoundPlayer \'C:\\Windows\\Media\\Alarm01.wav\').PlaySync();" > /dev/null 2>&1' if os.name == 'nt' else '')

print(f"{YELLOW}J25 ACTIF → Alerte Discord + COULEURS + SON (Ctrl+C pour arrêter){RESET}")

while True:
    errors = count_word("error_log.txt", "ERROR")
    
    if errors >= 5:
        msg = f"**ALERTE ROUGE FRÉRO !** {errors} erreurs → Incendie en cours !!"
        send_discord(msg)
        print(f"{RED}{BOLD}[{time.strftime('%H:%M:%S')}] ALERTE ROUGE → {errors} erreurs !!!!{RESET}")
        beep()           # ← SIRÈNE PC
        time.sleep(1)    # petit délai pour que le son soit bien entendu
    else:
        print(f"{GREEN}[{time.strftime('%H:%M:%S')}] Tout calme ({errors} erreurs){RESET}")

    time.sleep(10)
