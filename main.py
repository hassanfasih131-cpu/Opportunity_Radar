import requests

#Public API containing job listings.
url = "https://remotive.com/api/remote-jobs"
def collect_data():
    #Collecting job opportunities from the public API.
    try:
        response = requests.get(url, timeout=10)
        #Raises an exception
        response.raise_for_status()
        #Convert the JSON response into a Python dictionary.
        data = response.json()
        #Stores the job listing
        jobs = data.get("jobs", [])
        print(f"Collected {len(jobs)} jobs from Remotive.")
        return jobs
    except requests.exceptions.Timeout:
        #Exception if it takes too long
        print("ERROR: The data source timed out.")
        return []

    except requests.exceptions.RequestException as e:
        #Other Exceptions.
        print(f"ERROR: Could not collect job data: {e}")
        return []

    except ValueError:
        #Value Error
        print("ERROR: Value Error.")
        return []
#Test
#print(collect_data())