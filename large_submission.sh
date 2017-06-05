#!/bin/bash

for txt in $(ls runlists/runlist*txt)
do
    #echo $txt
    ./submit_jobs.sh $txt
    sleep 1
done
