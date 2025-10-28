#!/usr/bin/env python3

count = 0
with open("error_log.txt", "r") as file:
    for line in file:
        if "ERROR" in line:
            count += 1
print("Nombre d'erreurs :", count)
