from encodings import utf_8

import requests
import datetime
from datetime import datetime
#Public API containing job listings.
url = "https://remotive.com/api/remote-jobs"
def collect_data():
    #Collecting job opportunities from the public API.
    try:
        response = requests.get(url,params={"search":"marketing","limit":50}, timeout=10)
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

def filter_data(jobs):
    #filter and rank marketing opportunities
    keywords=["marketing","advertising","digital marketing", "social media", "seo", "content marketing"] #keywords
    count=0 #score points
    store=[]
    for i in jobs:
        title=i.get("title")
        description=i.get("description")
        job=(title+": "+description).lower() #combining the title and description
        for j in keywords:
            if j in job:
                count+=10
        #location information
        location = i.get("candidate_required_location","").lower()
        if "worldwide" in location.lower():
            count += 10
        job_type=i.get("job_type","").lower()
        #helping find entry level positions
        if job_type=="internship":
            count += 10
        #ignoring non entry level positions
        if "senior" "executive" "lead" "mid-level" in title.lower():
            continue
        if count>0:
            #stores the calculated score
            i["relevance_score"]=count
            store.append(i)
    store.sort(key=lambda job: job["relevance_score"], reverse=True)
    print(f"{len(store)} jobs matched our criteria.")
    return store
def generate_dashboard(options):
    creation_time=str(datetime.now()) #The time the dashboard was created
    #Storing the HTML code inside a variable to be used later in a .html file
    html=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>
            Digital Marketing Opportunities Radar
        </title>
    </head>
    <body>
    <h1>
            Digital Marketing Opportunities Radar
    </h1>
    <p>
        <strong>Generated on {creation_time}</strong>
    </p>
    <p>
        <strong>Data Source from Remotive</strong>
    </p>
    """
    #if there are no opportunities
    if not options:
        html+="""
        <p>
            No opportunities was found
        </p>
        """
    #Adding all the jobs found in the dashboard
    for i in options:
        title=i.get("title","unknown")
        company_name=i.get("company_name","unknown")
        category=i.get("category","unknown")
        job_type=i.get("job_type","unknown")
        location=i.get("candidate_required_location","unknown")
        salary=i.get("salary","unknown")
        URL=i.get("url","#")
        score=i.get("relevance_score",0)
        #Adding API into html
        html += f"""
            <div>

                <h3>
                    {title}
                </h3>

                <p>

                    <strong>Company:</strong>
                    {company_name}

                    <br>

                    <strong>Category:</strong>
                    {category}

                    <br>

                    <strong>Job Type:</strong>
                    {job_type}

                    <br>

                    <strong>Location:</strong>
                    {location}

                    <br>

                    <strong>Salary:</strong>
                    {salary}

                    <br>

                    <strong>Relevance Score:</strong>
                    {score}

                </p>

                <a
                    href="{url}"
                    target="_blank"
                >
                    View Job on Remotive
                </a>

            </div>

            <hr>
        """
        #Saving the HTML file
        with open("GeneratedOutput.html","w",encoding="utf_8") as f:
            f.write(html)
        print("Dashboard generated")