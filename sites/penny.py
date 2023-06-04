from scraper_peviitor import Scraper, Rules, loadingData
import uuid

url = "https://cariere.penny.ro/joburi/"
scraper = Scraper(url)
rules = Rules(scraper)

#Setam pagina pe care vrem sa o extragem
pageNum = 1 

#Cautam elementele care contin joburile si locatiile
jobs = rules.getTags("div", {"class": "job_position"})

finalJobs = list()

#Pentru fiecare job, extragem titlul, link-ul, compania, tara si orasul
while jobs:
    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("span", {"itemprop": "title"}).text.strip()
        job_link = job.find("a", {"itemprop": "url"}).get("href")
        company = "Penny"
        country = "Romania"
        try: 
            city = job.find("span", {"itemprop": "addressLocality"}).text.strip()
        except:
            city = "Romania"
        print(job_title + " -> " + city)

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company,
            "country": country,
            "city": city
        })
    #Setam pagina urmatoare
    pageNum += 1
    #Setam link-ul paginii
    scraper.url = url + f"page/{pageNum}/"
    #Cautam elementele care contin joburile si locatiile
    jobs = rules.getTags("div", {"class": "job_position"})

#Afisam numarul total de joburi gasite
print("Total jobs: " + str(len(finalJobs)))

#Incarcam datele in baza de date
loadingData(finalJobs, "Penny")
