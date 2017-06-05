#!/bin/bash

###  takes 1 argument ###
# 1: name (and path if necessary) to runlist txt file

### format of runlist txt file ###
# 1. noise
# 2. bottom run
# 3. top bulk run
# 4. top ring run


# check if log dir exists
if [[ ! -e ./logs ]]; then
    mkdir logs
fi

noise_run=$(head -n 1 $1)
LED_runs=$(tail -n +2 $1)

echo "noise run: $noise_run"
echo "LED runs: $LED_runs"

# setup rucio stuff

#where we will save the raw data
tmp_dir="/project/lgrandi/shockley/rucio_downloads"

# env stuff
source activate pax_head
export PYTHONPATH=/project/lgrandi/anaconda3/envs/pax_head/lib/python3.4/site-packages:$PYTHONPATH
noise_DID=$( python get_rucio_did.py $noise_run)
noise_name=$( python get_name.py $noise_run)

# download noise run
if [[ ! -e $tmp_dir/$noise_name ]]; then
    source /project/lgrandi/general_scripts/setup_rucio.sh
    mkdir $tmp_dir/$noise_name
    rucio download $noise_DID --dir $tmp_dir/$noise_name --no-subdir
fi

sleep 2

# loop over LED_runs, submit jobs that download LED run and do runs spe_acceptance code
for run in $LED_runs; do
    DID=$(python get_rucio_did.py $run)
    name=$(python get_name.py $run)
    sbatch_script=./sbatch_scripts/$run.sbatch
    cat <<EOF > $sbatch_script
#!/bin/bash
#SBATCH --job-name=spe_accept_$run
#SBATCH --output=${PWD}/logs/run_${run}_%J.log
#SBATCH --error=${PWD}/logs/run_${run}_%J.log
#SBATCH --account=pi-lgrandi
#SBATCH --qos=xenon1t
#SBATCH --partition=xenon1t

export PATH=/project/lgrandi/anaconda3/bin:$PATH
source activate pax_head
source /project/lgrandi/general_scripts/setup_rucio.sh

if [[ ! -e $tmp_dir/$name ]]; then
    mkdir $tmp_dir/$name
    echo "rucio download $DID --dir $tmp_dir/$name --no-subdir"
    rucio download $DID --dir $tmp_dir/$name --no-subdir
fi

export PYTHONPATH=/project/lgrandi/anaconda3/envs/pax_head/lib/python3.4/site-packages:$PYTHONPATH

/home/ershockley/analysis/old_analysis/spe_acceptance/spe_acceptance.py $run $noise_run $tmp_dir/$name $tmp_dir/$noise_name

EOF

    sbatch $sbatch_script
    sleep 1
done
