#!/bin/bash
nmap 127.0.0.1 | grep open > test_ports.txt
cat test_ports.txt

