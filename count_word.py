#!/usr/bin/env python3

def count_word(fichier, mot):
    c = 0
    with open(fichier, "r") as file:
        for line in file:
            if mot in line:
                c += 1
    return c

print("INFO:", count_word("error_log.txt", "INFO"))
print("ERROR:", count_word("error_log.txt", "ERROR"))
