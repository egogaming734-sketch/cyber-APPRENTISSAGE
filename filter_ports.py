#!/usr/bin/python3
with open("ports.txt", "r") as file:
    for line in file:
        if "open" in line:
            print(line.strip())