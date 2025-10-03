#!/bin/bash
echo "aller on extrait la date des echecs de conexions :"
grep "SUCCESS" server.log | awk '{print $1}'
