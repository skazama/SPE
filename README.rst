===================
SPE Acceptance Code
===================
Evan Shockley

email: ershockley@uchicago.edu


Overview
--------

This folder contains several scripts (bash and python) and notebooks that are used to calculate/analyze SPE acceptance. To extract the SPE acceptance, we take low intensity LED runs and a 'blank' run, which is externally triggered just as an LED run but with no light emitted. By subtracting the blank amplitude spectrum from the LED amplitude spectrum, we can extract the SPE amplitude distribution and from there easily calculate the acceptance as a function of amplitude (or threshold).

One complication to the code is that, due to non-uniform LED exposure to PMTs, we need to take 3 different SPE acceptance LED runs. Therefore we need to pair runs together in a runlist.txt which is used to submit jobs for each LED run, then kinda splice the results together at the end. 


How to run the code
-------------------

It is preferred to submit to xenon1t nodes from midway2 (ssh <user>@midway2.rcc.uchicago.edu). 
You must be in a pax environment (pax_head should be fine).
    source activate pax_head
    
You must execute all scripts from inside the spe_acceptance directory since the code uses relative paths currently.

`make_runlist.py` uses the RunsDB to pair SPE acceptance runs with blank runs and write a text file that is used in various parts of the analysis. It has a dry-run mode, so

  python make_runlist.py

can be used to make sure runs are getting paired up correctly, and

  python make_runlist.py write

actually writes the files to the `runlists` directory.

If you want to submit jobs for one runlist, you can do

  ./submit_jobs.sh <runlist>
  
or use `large_submission.sh` to submit jobs for all runlists in a directory (skipping runs who have data directories inside `data`).

These jobs download the raw data if needed, and then execute the python script `spe_acceptance.py`, which processes the raw data and writes to csv files in the `data` directory.

After the jobs finish, you can use the Jupyter notebooks to analyze data (mostly using the analyze.py module) and write to the `acceptance_data` directory, which contains files with the acceptance fraction for each channel as calculated using the 3 LED runs listed.

email me with any questions or problems, tried to keep this short.




