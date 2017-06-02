#!/bin/bash
#SBATCH --job-name=spe_accept_5245
#SBATCH --output=/home/ershockley/xenon1t/analysis/spe_acceptance/logs/run_5245_%J.log
#SBATCH --error=/home/ershockley/xenon1t/analysis/spe_acceptance/logs/run_5245_%J.log
#SBATCH --account=kicp
#SBATCH --qos=kicp
#SBATCH --partition=kicp

export PATH=/project/lgrandi/anaconda3/bin:/project/lgrandi/anaconda3/envs/pax_head/bin:/project/lgrandi/anaconda3/envs/pax_head/bin:/software/slurm-current-el6-x86_64/bin:/software/connect-client-0.5.2-el6-x86_64/bin:/software/python-2.7-2015q2-el6-x86_64/bin:/software/gdal-1.11-el6-x86_64/bin:/software/proj-4.9-el6-x86_64/bin:/software/postgresql-9.2-el6-x86_64/bin:/software/geos-3.4-el6-x86_64/bin:/software/qt-4.8-el6-x86_64/bin:/software/graphviz-2.28-el6-x86_64/bin:/software/netcdf-4.2-el6-x86_64/bin:/software/hdf5-1.8-el6-x86_64/bin:/software/texlive-2012-el6-x86_64/bin/x86_64-linux/:/software/texlive-2012-el6-x86_64/bin:/software/git-2.7-el6-x86_64/bin:/software/emacs-24-el6-x86_64/bin:/software/subversion-1.8-el6-x86_64/bin:/software/vim-7.4-el6-x86_64/bin:/software/bin:/srv/adm/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/lpp/mmfs/bin:/home/ershockley/bin:/home/ershockley/bin
source activate pax_head

/home/ershockley/xenon1t/analysis/spe_acceptance/spe_acceptance.py 5245 5239 
