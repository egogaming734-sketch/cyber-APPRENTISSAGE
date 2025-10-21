#!/usr/bin/python3
with open("ports.txt", "r") as file:
    for line in file:
        if "open" in line:
            if "http" in line:
                print("HTTP Port:", line.strip())
            elif "https" in line:
                print("HTTPS Port:", line.strip())
            else:
                print("Other Port:", line.strip())