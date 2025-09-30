#!/bin/bash
echo "Utilisateurs avec échec de connexion :"
grep "FAILED" server.log | awk '{print $3}'

