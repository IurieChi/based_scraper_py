from scraper_peviitor import Scraper, loadingData, Rules
import uuid
import json

url = "https://jobs.parexel.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=100&Distance=50&RadiusUnitType=0&Location=Romania&Latitude=46.00000&Longitude=25.00000&ShowRadius=False&IsPagination=False&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=6&SortDirection=0&SearchType=1&LocationType=2&LocationPath=798549&OrganizationIds=877&ResultsType=0"

company = {"company": "Parexel"}
finalJobs = list()

scraper = Scraper(url)
rules = Rules(scraper)

html = scraper.getJson().get("results")
scraper.soup = html

jobs = rules.getTags("li")

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("h2").text
    job_link = "https://jobs.parexel.com" + job.find("a").get("href")
    city = ""

    if job.find("span", {"class": "job-city"}) is not None:
        city = job.find("span", {"class": "job-city"}).text.strip()
    else:
        city = job.find("span", {"class": "job-location"}).text.split(",")[0].strip()

    print(job_title + " -> " + city)

    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "company": company.get("company")
    })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", company.get("company"))

logoUrl = "https://www.parexel.com/application/files/7915/5664/0483/Parexel_Master_Logo_RGB.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))