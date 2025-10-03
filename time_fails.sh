#!/bin/bash
echo "Horaires des échecs de connexion :" # Titre
grep "FAILED" server.log | awk '{print $2}' # Extrait heure
