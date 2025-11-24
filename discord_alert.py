#!/usr/bin/env python3
import requests
import time

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

print("J24 ACTIF → Alerte Discord en live (Ctrl+C pour arrêter)")

while True:
    errors = count_word("error_log.txt", "ERROR")
    
    if errors >= 5:
        send_discord(f"**ALERTE ROUGE FRÉRO !** {errors} erreurs détectées ! Incendie en cours !")
        print(f"[{time.strftime('%H:%M:%S')}] ALERTE ROUGE envoyée → {errors} erreurs")
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Tout calme ({errors} erreurs)")

    time.sleep(10)
