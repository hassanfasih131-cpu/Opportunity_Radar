import json
import os
MEMORY_FILE = "data/job_memory.json"
def load_memory():
    #Load job IDs from the previous scan.
    if not os.path.exists(MEMORY_FILE):
        print("No previous memory found.")
        #Return an empty set
        return set()
    try:
        #Open the JSON memory file.
        with open(MEMORY_FILE,"r",encoding="utf-8") as f:
            memory = json.load(f)
        # Gets the list of job IDs that was previously saved, otherwise it would return an empty set
        previous_ids = memory.get("seen_job_ids",[])
        return set(previous_ids)
    except json.JSONDecodeError:
        print("ERROR: Invalid Json file or file was previously empty")
        return set()
    except OSError:
        print(f"ERROR: Could not read the memory file") #error of file not being opening
        return set()

def find_new_jobs(jobs, previous_ids):
    current_ids=set()
    new_jobs=[]
    #looks at every job returned
    for i in jobs:
        job_id = i.get("id")
        if job_id is None:
            continue
        current_ids.add(job_id)
        if job_id not in previous_ids: #if the job was not in the earlier scan
            i["is_new"]=True
            new_jobs.append(i)
        else:
            i["is_new"] = False #if the job was in the earlier scan
    print(f"New jobs detected: {len(new_jobs)}")
    return new_jobs, current_ids
def save_memory(job_ids):
    os.makedirs("data",exist_ok=True)
    #Creates the dictionary that will become JSON
    memory = {"seen_job_ids": list(job_ids)}
    try: #Convert the Python dictionary into JSON.
        with open(MEMORY_FILE,"w",encoding="utf-8") as f:
            json.dump(memory,f,indent=4)
        print(f"Memory saved successfully: "f"{len(job_ids)} job IDs.")
    except OSError:
        print(f"ERROR: Could not save memory")