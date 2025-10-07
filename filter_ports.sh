#!/bin/bash
echo "filtrons les ports ouverts :"
nmap localhost | grep open > ports.txt
cat ports.txt
