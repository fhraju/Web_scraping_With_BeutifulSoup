from bs4 import BeautifulSoup
import requests
import time

# print("Put some skill you don't have: ")
# skill_dont_have = input(">  ")
# print(f"Filtering Out: {skill_dont_have}")

def jobs_search():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=').text

    soup_instance = BeautifulSoup(html_text, 'lxml')

    jobs = soup_instance.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for index, job in enumerate(jobs):
        posted_date = job.find('span', class_='sim-posted').span.text
        if 'few days' in posted_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ','')
            skill_requirement = job.find('span', class_ ='srp-skills').text.replace(' ','')
            more_info_link = job.header.h2.a['href']

            # if skill_dont_have not in skill_requirement:
            with open(f'timesjobsposts/{index}.txt', 'w') as f:
                f.write(f"Company Name: {company_name.strip()}\n")
                f.write(f"Skills Requirement: {skill_requirement.strip()}\n")
                f.write(f"More Informations Link: {more_info_link}")
            print(f"File saved: {index}")

if __name__ == '__main__':
    while True:
        jobs_search()
        time_wait = 10
        print(f"\nWaiting {time_wait} minutes...\n")
        time.sleep(time_wait * 60)