import pymongo
import os
import sys

uri = 'mongodb://eb:%s@xenon1t-daq.lngs.infn.it:27017,copslx50.fysik.su.se:27017,zenigata.uchicago.edu:27017/run'
uri = uri % os.environ.get('MONGO_PASSWORD')
c = pymongo.MongoClient(uri,
                        replicaSet='runs',
                        readPreference='secondaryPreferred')
db = c['run']
collection = db['runs_new']

def get_last_run(path):
    numbers = sorted([int(f.split("_")[1]) for f in os.listdir(path) if "run_" in f])
    lastrun = numbers[-1]
    return lastrun

def spe_run_counter(write = False):
    #last_run = get_last_run("./data")
    query = {"detector":"tpc", 
             "source.type" : "LED",
             "tags" : {"$exists" : True},
             "comments": {"$exists" : True}
    #         "number" : {"$gt" : last_run}
            }
    
    cursor = collection.find(query, {"number" : True,
                                     "data" : True,
                                     "comments" : True,
                                     "tags" : True,
                                     "trigger.events_built" : True,
                                     "_id":False})
    cursor = list(cursor)

    if not write:
        print("cursor has %d runs" % len(cursor))
        
    spe_runs = []
    spe_bottom = []
    spe_topbulk = []
    spe_topring = []
    spe_blank = []
    
    missing_runs = []


    # this is an absolute mess, but tries to figure out which runs are which configuration
    for run in cursor:
        
        if any(["bad" in t["name"] for t in run["tags"]]):
            continue
        # make sure we're only considering the long LED runs 
        if "events_built" not in run["trigger"] or run["trigger"]["events_built"] < 100000:
            continue
        
        if any(["Gain step_4" in com["text"] or "SPE acceptance step_0" in com["text"] or "LED calibration step 4" in com["text"] or "LED calibration, step 4" in com["text"] or "LED Calibration step 4" in com["text"] or "LED Calibration: step 4" in com['text'] or "LED Gain Calibration step4" in com['text'] or "http://wims.univ-savoie.fr/wims/" in com['text'] for com in run["comments"]]):
            spe_blank.append(run["number"])
            
        if any(["SPE" in com["text"] for com in run["comments"]]):
                
            if any(["topbulk" in com["text"] or "step_2" in com["text"] or "step 2" in com["text"]  or "3.7, 3.7, 3.8" in com["text"] for com in run["comments"]]):
                spe_topbulk.append(run["number"])
                    
            if any(["topring" in com["text"] or "step_3" in com["text"] or "step 3" in com["text"] or "3.84, 3.84, 3.94" in com["text"] or "topouter" in com['text'] or "TopRing" in com['text'] for com in run["comments"]]):
                spe_topring.append(run["number"])
                    
            if any(["bottom" in com["text"] or "step_1" in com["text"] or "step 1" in com["text"] or "3.6, 3.6, 3.7" in com["text"] for com in run["comments"]]):
                spe_bottom.append(run["number"])
            
            spe_runs.append(run["number"])

    for L in [spe_blank, spe_bottom, spe_topbulk, spe_topring]:
        remove_list = []
        for run in L:
            for r in L:
                if r <= run:
                    continue
                if abs(r-run) < 10:
                    remove_list.append(run)
        remove_list = list(set(remove_list))
        for r in remove_list:
            L.remove(r)
        
        blank_remove = []
        for blank in spe_blank:
            if not any([abs(blank - LED) < 10 for LED in spe_bottom]):
                blank_remove.append(blank)
            
        for b in list(set(blank_remove)):
            spe_blank.remove(b)

    print("blank" , len(spe_blank))
    print("bottom", len(spe_bottom))
    print("topbulk", len(spe_topbulk))
    print("topring", len(spe_topring))

    for blank, bot, bulk, ring in zip(spe_blank, spe_bottom, spe_topbulk, spe_topring):
        filename = "./runlists/runlist_%i_%i_%i.txt" % (bot, bulk, ring)
        if not os.path.exists(filename):
            if write:
                with open(filename, "w") as f:
                    f.write("%i\n" %blank)
                    f.write("%i\n" %bot)
                    f.write("%i\n" %bulk)
                    f.write("%i\n" %ring)
            else:
                print("%d %d %d %d" % (blank, bot, bulk, ring))
            
if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("writing these runs to files")
        write = True
    else:
        print("Dry run. These runs would be downloaded and analyzed.")
        write = False
    spe_run_counter(write)


