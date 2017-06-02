#!/bin/bash
#SBATCH --job-name=spe_accept_9797
#SBATCH --output=/home/ershockley/analysis/old_analysis/spe_acceptance/logs/run_9797_%J.log
#SBATCH --error=/home/ershockley/analysis/old_analysis/spe_acceptance/logs/run_9797_%J.log
#SBATCH --account=pi-lgrandi
#SBATCH --qos=xenon1t
#SBATCH --partition=xenon1t

echo 

export PATH=/project/lgrandi/anaconda3/bin:/project/lgrandi/anaconda3/envs/pax_head/bin:/project/lgrandi/anaconda3/envs/pax_head/bin:/project/lgrandi/anaconda3/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el7-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el7-x86_64/usr/sbin:/bin:/software/slurm-current-el7-x86_64/bin:/project/lgrandi/anaconda3/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el7-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el7-x86_64/usr/sbin:/bin:/software/git-2.10-el7-x86_64/bin:/software/subversion-1.9.4-el7-x86_64/bin:/software/bin:/srv/adm/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/ibutils/bin:/usr/lpp/mmfs/bin:/home/ershockley/bin
source activate pax_head
source /project/lgrandi/general_scripts/setup_rucio.sh

if [[ ! -e /project/lgrandi/shockley/rucio_downloads/170523_0819 ]]; then
    mkdir /project/lgrandi/shockley/rucio_downloads/170523_0819
    echo "rucio download x1t_SR001_170523_0819_tpc:raw --dir /project/lgrandi/shockley/rucio_downloads/170523_0819 --no-subdir"
    rucio download x1t_SR001_170523_0819_tpc:raw --dir /project/lgrandi/shockley/rucio_downloads/170523_0819 --no-subdir
fi

export PYTHONPATH=/project/lgrandi/anaconda3/envs/pax_head/lib/python3.4/site-packages:/project/lgrandi/anaconda3/envs/pax_head/lib/python3.4/site-packages:/project/lgrandi/anaconda3/envs/pax_head/lib:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el7-x86_64/usr/lib/python2.7/site-packages:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el7-x86_64/usr/lib64/python2.7/site-packages:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el7-x86_64/usr/lib/python2.7/site-packages:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el7-x86_64/usr/lib64/python2.7/site-packages

/home/ershockley/analysis/old_analysis/spe_acceptance/spe_acceptance.py 9797 9796 /project/lgrandi/shockley/rucio_downloads/170523_0819 /project/lgrandi/shockley/rucio_downloads/170523_0809

