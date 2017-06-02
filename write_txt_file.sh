#!/bin/bash

###  takes 1 argument ###
# 1: name (and path if necessary) to runlist txt file

### format of runlist txt file ###
# 1. noise
# 2. bottom run
# 3. top bulk run
# 4. top ring run


noise_run=$(head -n 1 $1)
LED_runs=$(tail -n +2 $1)

bottom_run=$(echo $LED_runs | awk '{print $1}')
topbulk_run=$(echo $LED_runs | awk '{print $2}')
topring_run=$(echo $LED_runs | awk '{print $3}')

echo "noise run: $noise_run"
echo "LED runs: $LED_runs"

filename="acceptances_$noise_run.txt"

python analyze.py $filename $bottom_run $topbulk_run $topring_run

