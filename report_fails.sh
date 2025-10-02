#!/bin/bash
echo "Rapport des échecs de connexion :"
echo "Nombre d'échecs :"
grep "FAILED" server.log | wc -l
echo "Utilisateurs en échec :"
grep "FAILED" server.log | awk '{print $4}'
