import pymongo
import os
import sys
import subprocess
import numpy as np

default_rucio_out = "/project/lgrandi/shockley/rucio_downloads"

uri = 'mongodb://eb:%s@xenon1t-daq.lngs.infn.it:27017,copslx50.fysik.su.se:27017,zenigata.uchicago.edu:27017/run'
uri = uri % os.environ.get('MONGO_PASSWORD')
c = pymongo.MongoClient(uri,
                        replicaSet='runs',
                        readPreference='secondaryPreferred')
db = c['run']
collection = db['runs_new']

def rucio_download(rucio_loc, output_dir = default_rucio_out):
    # not used currently
    print("downloading from rucio...")
    rucio_command = ["rucio", "download", rucio_loc, "--dir", output_dir, "--no-subdir"]
    print(rucio_command)
    execute = subprocess.Popen(rucio_command,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=False,
                               universal_newlines=False)
    stdout_value, stderr_value = execute.communicate()
    stdout_value = stdout_value.decode("utf-8")
    stdout_value = stdout_value.split("\n")
    stdout_value = list(filter(None, stdout_value))
    for line in stdout_value:
        print(line)

    print("done.")


def get_file_path(run_number):
    query = {"detector":"tpc", "number":run_number}

    cursor = collection.find(query, {"number" : True,
                                     "name": True,
                                     "trigger.events_built"
                                     "data" : True,
                                     "_id":False})

    cursor = list(cursor)
    entry_list = cursor[0]['data']
    events = cursor[0]['trigger']['events_built']
    run_name = cursor[0]["name"]

    # check if on midway, rucio
    on_midway = False
    on_rucio = False
    midway_loc = None
    rucio_loc = None

    for entry in entry_list:
        if entry["host"] == "midway-login1" and entry["type"] == 'raw':
            midway_loc = entry["location"]
            if '/project2' not in midway_loc:
                on_midway = True
        elif entry['host'] == "rucio-catalogue" and entry["type"] == 'raw':
            on_rucio = True
            rucio_loc = entry["location"]

    use_rucio = on_rucio and not on_midway


    # if use rucio...
    if use_rucio:
        # first have to download
        path = default_rucio_out + "/" + run_name
        if not os.path.exists(path):
            print("Data not on midway, downloading with rucio")
            rucio_download(rucio_loc, path)
        else:
            nzips = len([f for f in os.listdir(path) if f.startswith('XENON')])
            if not any( [f.startswith('XENON') for f in os.listdir(path)] ):
                print("Seems like incomplete transfer. Downloading again")
                rucio_download(rucio_loc, path)
            else:
                print("already downloaded at %s" % path)
                
        # ...then the data is stored at this path:
    #    path = default_rucio_out + "/%s" % rucio_loc.split(":")[0]

    # if not, just get path directly from midway

    else:
        path = midway_loc

    return path


def find_regular_run(LED_run):
    query = {'source.type': {'$ne': 'LED'},
             '$and': [{'number': {'$lt': LED_run + 20}},
                      {'number': {'$gt': LED_run - 20}}
                      ]
             }
    cursor = collection.find(query, {'number': True,
                                     'reader': True,
                                     '_id': False})

    runs = np.array([run['number'] for run in cursor
                     if any([r['register'] == '8060'
                             for r in run['reader']['ini']['registers']])])

    if LED_run < 5144:  # when thresholds changed
        runs = runs[runs < 5144]
    elif LED_run > 5144:
        runs = runs[runs > 5144]
    diff = abs(runs - LED_run)

    closest_run = runs[np.argmin(diff)]

    return closest_run


if __name__ == "__main__":
    get_file_path(4512)
