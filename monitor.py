#!/usr/bin/env python3
import time

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

print("MONITORING ACTIF — Ctrl+C pour arrêter")

while True:
    errors = count_word("error_log.txt", "ERROR")
    infos  = count_word("error_log.txt", "INFO")
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] INFO: {infos} | ERROR: {errors}", end="")
    
    if errors >= 5:
        print("  ALERTE ROUGE !")
    elif errors >= 3:
        print("  ALERTE ORANGE")
    else:
        print()
    
    time.sleep(10)
