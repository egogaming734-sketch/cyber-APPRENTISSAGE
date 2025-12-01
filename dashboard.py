#!/usr/bin/env python3
import time
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1442275533697060874/Hd0j2d2Eo--ECxJCnuO2XVxga4KzMzWMDcU96JDWv6tv1fKGZTIDrOJewi8vNMEnC5nc"

def send_discord(message):
    os.system(f'curl -H "Content-Type: application/json" -d \'{{"content": "{message}"}}\' {WEBHOOK_URL}')

def count_word(fichier, mot):
    try:
        with open(fichier, "r") as f:
            return sum(1 for line in f if mot in line)
    except:
        return 0

def clear(): os.system('clear' if os.name == 'posix' else 'cls')

print("\033[93m" + " " * 20 + "MINI-SIEM MAISON — J27 " + "\033[0m")
time.sleep(3)

while True:
    clear()
    errors = count_word("error_log.txt", "ERROR")
    infos  = count_word("error_log.txt", "INFO")
    timestamp = time.strftime("%d/%m %H:%M:%S")

    bar_length = 30
    error_percent = min(errors / 10 * 100, 100) if errors else 0
    filled = int(bar_length * error_percent // 100)
    bar = "█" * filled + "░" * (bar_length - filled)

    print(f"\033[96m╔{'═' * 48}╗\033[0m")
    print(f"\033[96m║ MINI-SIEM FRÉRO               {timestamp}  ║\033[0m")
    print(f"\033[96m╠{'═' * 48}╣\033[0m")
    print(f"  INFO   : {infos:>4}   │  ⚠️  ERROR  : \033[91m{errors:>4}\033[0m")
    print(f"  NIVEAU DANGER : [{bar}] {error_percent:>3}%")
    print(f"\033[96m╚{'═' * 48}╝\033[0m")

    if errors >= 5:
        send_discord(f"**ALERTE ROUGE** → {errors} erreurs ! Dashboard en feu !")
        print("\033[91m" + " " * 15 + "ALERTE ROUGE ENVOYÉE SUR DISCORD " + "\033[0m")
        os.system('echo -e "\a"')
    else:
        print(" " * 15 + "\033[92mTout est calme pour l'instant…\033[0m")

    time.sleep(5)
