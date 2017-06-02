#!/bin/bash
#SBATCH --job-name=spe_accept_9604
#SBATCH --output=/project/lgrandi/xenon1t/spe_acceptance/logs/run_9604_%J.log
#SBATCH --error=/project/lgrandi/xenon1t/spe_acceptance/logs/run_9604_%J.log
#SBATCH --account=kicp
#SBATCH --partition=kicp

echo 

export PATH=/project/lgrandi/anaconda3/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el6-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el6-x86_64/usr/sbin:/cvmfs/xenon.opensciencegrid.org/software/rucio-py26/1.8.3/bin:/project/lgrandi/anaconda3/envs/pax_head/bin:/project/lgrandi/anaconda3/envs/pax_head/bin:/project/lgrandi/anaconda3/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el6-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el6-x86_64/usr/sbin:/software/slurm-current-el6-x86_64/bin:/software/git-2.7-el6-x86_64/bin:/software/emacs-24-el6-x86_64/bin:/software/subversion-1.8-el6-x86_64/bin:/software/vim-7.4-el6-x86_64/bin:/software/bin:/srv/adm/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/lpp/mmfs/bin:/home/ershockley/bin
source activate pax_head
source /home/ershockley/setup_rucio.sh

source /cvmfs/xenon.opensciencegrid.org/software/rucio-py26/setup_rucio_1_8_3.sh
export RUCIO_ACCOUNT=xenon-analysis
export X509_USER_PROXY=/project/lgrandi/xenon1t/grid_proxy/xenon_service_proxy

#module load Anaconda2
#export PYTHONPATH=/software/Anaconda2-4.3.0-el7-x86_64/lib/python2.7/site-packages/:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el6-x86_64/usr/lib/python2.6/site-packages:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el6-x86_64/usr/lib64/python2.6/site-packages:/cvmfs/xenon.opensciencegrid.org/software/rucio-py26/1.8.3/lib/python2.6/site-packages:/project/lgrandi/anaconda3/envs/pax_head/lib:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el6-x86_64/usr/lib/python2.6/site-packages:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.24/el6-x86_64/usr/lib64/python2.6/site-packages

if [[ ! -e /project/lgrandi/shockley/rucio_downloads/170516_1158 ]]; then
    mkdir /project/lgrandi/shockley/rucio_downloads/170516_1158
    rucio download x1t_SR001_170516_1158_tpc:raw --dir /project/lgrandi/shockley/rucio_downloads/170516_1158 --no-subdir
fi

#sleep 350s
/home/ershockley/analysis/old_analysis/spe_acceptance/spe_acceptance.py 9604 9603 /project/lgrandi/shockley/rucio_downloads/170516_1158 /project/lgrandi/shockley/rucio_downloads/170516_1145

