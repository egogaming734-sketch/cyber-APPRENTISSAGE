#!/bin/bash
echo "nombre de conexion :"
grep "FAILED" server.log | wc -l

