#!/usr/bin/env python3

def count_word(fichier, mot):
    c = 0
    with open(fichier, "r") as file:
        for line in file:
            if mot in line:
                c += 1
    return c

infos = count_word("error_log.txt", "INFO")
errors = count_word("error_log.txt", "ERROR")

print(f"INFO : {infos}")
print(f"ERROR : {errors}")

if errors >= 5:
    print("ALERTE ROUGE : Incident critique ! 5+ erreurs détectées !!")
elif errors >= 3:
    print("ALERTE ORANGE : 3-4 erreurs, on surveille de près")
elif errors >= 1:
    print("Attention : Des erreurs sont présentes.")
else:
    print("Tout va bien, système stable.")
