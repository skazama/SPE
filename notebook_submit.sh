#!/bin/bash

for file in $(cat tmp_submit_file.txt)
do
    ./submit_jobs.sh $file
done

