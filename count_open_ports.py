#!/usr/bin/python3
count = 0
with open("ports.txt", "r") as file:
    for line in file:
        if "open" in line:
            count += 1
print("Nombre de ports ouverts :", count)