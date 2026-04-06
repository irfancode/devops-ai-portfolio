#!/bin/bash
THRESHOLD_CPU=80
THRESHOLD_MEM=80

while true; do
  cpu=$(grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}')
  mem=$(free | awk '/Mem/{printf("%.0f"), $3/$2*100}')

  if (( ${cpu%.*} > THRESHOLD_CPU )); then
    echo "[$(date)] High CPU usage: ${cpu%.*}%"
  fi

  if (( mem > THRESHOLD_MEM )); then
    echo "[$(date)] High Memory usage: ${mem}%"
  fi

  sleep 30
done
