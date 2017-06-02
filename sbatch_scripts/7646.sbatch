#!/bin/bash
#SBATCH --job-name=spe_accept_7646
#SBATCH --output=/home/ershockley/xenon1t/analysis/spe_acceptance/logs/run_7646_%J.log
#SBATCH --error=/home/ershockley/xenon1t/analysis/spe_acceptance/logs/run_7646_%J.log
#SBATCH --account=kicp
#SBATCH --qos=kicp
#SBATCH --partition=kicp

export PATH=/project/lgrandi/anaconda3/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/sbin:/cvmfs/xenon.opensciencegrid.org/software/rucio-py26/1.8.3/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/sbin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/sbin:/cvmfs/xenon.opensciencegrid.org/software/rucio-py26/1.8.3/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/sbin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/sbin:/cvmfs/xenon.opensciencegrid.org/software/rucio-py26/1.8.3/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/sbin:/project/lgrandi/anaconda3/envs/pax_head/bin:/project/lgrandi/anaconda3/envs/pax_head/bin:/software/connect-client-0.5.2-el6-x86_64/bin:/software/python-2.7-2015q2-el6-x86_64/bin:/software/gdal-1.11-el6-x86_64/bin:/software/proj-4.9-el6-x86_64/bin:/software/postgresql-9.2-el6-x86_64/bin:/software/geos-3.4-el6-x86_64/bin:/software/qt-4.8-el6-x86_64/bin:/software/graphviz-2.28-el6-x86_64/bin:/software/netcdf-4.2-el6-x86_64/bin:/software/hdf5-1.8-el6-x86_64/bin:/software/texlive-2012-el6-x86_64/bin/x86_64-linux/:/software/texlive-2012-el6-x86_64/bin:/software/slurm-current-el6-x86_64/bin:/project/lgrandi/anaconda3/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/bin:/cvmfs/oasis.opensciencegrid.org/mis/osg-wn-client/3.3/3.3.22/el6-x86_64/usr/sbin:/software/git-2.7-el6-x86_64/bin:/software/emacs-24-el6-x86_64/bin:/software/subversion-1.8-el6-x86_64/bin:/software/vim-7.4-el6-x86_64/bin:/software/bin:/srv/adm/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/lpp/mmfs/bin:/home/ershockley/bin
source activate pax_head
#source /home/ershockley/setup_rucio.sh

source /cvmfs/xenon.opensciencegrid.org/software/rucio-py26/setup_rucio_1_8_3.sh
export RUCIO_ACCOUNT=ershockley
export X509_USER_PROXY=/home/ershockley/user_cert

if [[ ! -e /project/lgrandi/shockley/rucio_downloads/170306_1052 ]]; then
    mkdir /project/lgrandi/shockley/rucio_downloads/170306_1052
    rucio download x1t_SR000_170306_1052_tpc:raw --dir /project/lgrandi/shockley/rucio_downloads/170306_1052 --no-subdir
fi

#sleep 578s
/home/ershockley/xenon1t/analysis/spe_acceptance/spe_acceptance.py 7646 7645 /project/lgrandi/shockley/rucio_downloads/170306_1052 /project/lgrandi/shockley/rucio_downloads/170306_1042

