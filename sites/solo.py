import requests
from utils import publish_or_update, publish_logo, show_jobs

apiurl = "https://cariere.solo.ro/api/jobs/"
company = "SOLO"
logo = "https://cariere.solo.ro/assets/img/logo-black.svg"

raw_jobs = requests.get(apiurl + "list/").json()
jobs = []

for job in raw_jobs:
    title = job["Title"]
    city = "Bucuresti"
    county = "Bucuresti"
    country = "Romania"
    job_link = f"https://cariere.solo.ro/job/{job['Slug']}"

    jobs.append({
        "job_title": title,
        "job_link": job_link,
        "company": company,
        "country": country,
        "city": city,
        "county": county
    })

publish_or_update(jobs)

publish_logo(company, logo)
show_jobs(jobs)
