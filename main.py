from job_memory import (save_memory, find_new_jobs, load_memory)
import requests
import datetime
from datetime import datetime
#Public API containing job listings.
url = "https://remotive.com/api/remote-jobs"
def collect_data():
    #Collecting job opportunities from the public API.
    try:
        response = requests.get(url,params={"search":"marketing,sales","limit":50}, timeout=10)
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
    keywords=["marketing", "advertising", "digital marketing", "social media", "seo", "content marketing", "sales"]
    excluded=["software", "developer", "engineer", "technical writer", "data scientist", "devops", "frontend","backend"
              ,"writer", "reviewer", "editor"]
    store=[]
    for i in jobs:
        count = 0  # score points
        title=i.get("title","").lower()
        description=i.get("description","").lower()
        job=f"{title}: {description}" #combining the title and description
        senior_terms = ["senior", "executive", "lead", "director", "manager", "head"
            , "sr.","vice president", "v.p.", "chief","principal"]
        if any(term in title for term in senior_terms):
            continue
        matches = [kw for kw in keywords if kw in job]
        if not matches:
            continue
        count += len(matches) * 10
        if any(ex in title for ex in excluded):
            continue
        location = i.get("candidate_required_location", "").lower()
        if "worldwide" in location:
            count += 10
        job_type = i.get("job_type", "").lower()
        if job_type == "internship" or "intern" in title or "junior" in title or "entry" in title:
            count += 10
        if count > 0:
            i["relevance_score"] = count
            store.append(i)
    # Rank by score highest to lowest
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
            Digital Marketing or Sales Opportunities Radar
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
def main():
    options=collect_data()
    if not options:
        print("No options provided")
        return
    filter=filter_data(options)
    previous_ID=load_memory()
    new_jobs,current_ID = find_new_jobs(filter,previous_ID)
    save_memory(current_ID)
    DASHBOARD=generate_dashboard(filter)
    print("Scan Completed")

main()