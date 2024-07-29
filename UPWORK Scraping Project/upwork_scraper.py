from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

service=Service(executable_path='../chromedriver.exe')
driver=webdriver.Chrome(service=service)

data={'JOB_title':[],'JOB_salary':[],'Experience_Required':[],'Posted_on':[],'skills_required':[],'job_link':[]}

query='data analyst'
def main():
    try:
        driver.implicitly_wait(10)
        for page in range(1,10):
            print("page: ",page)
            driver.get(f'https://www.upwork.com/nx/search/jobs/?q={query}&page={page}')
            html=driver.page_source
            soup=BeautifulSoup(html,'lxml')
            tags1=soup.find_all('article',attrs={'class':"job-tile cursor-pointer px-md-4 air3-card air3-card-list px-4x"})


            for tag in tags1:
                # finding job titles
                if tag.a == None:
                    job_title='-'
                else:
                    job_title=tag.a.text
                data['JOB_title'].append(job_title)
                print(job_title)

                #finding salary per job
                if tag.li==None:
                    salary='-'
                else:
                    salary=tag.li.text
                data['JOB_salary'].append(salary)

                #finding experience required
                if tag.find('li',attrs={'data-test':"experience-level"})==None:
                    level='-'
                else:
                    level=tag.find('li',attrs={'data-test':"experience-level"}).text
                data['Experience_Required'].append(level)

                #finding job posting time
                if tag.find('small',attrs={'data-test':"job-pubilshed-date"})==None:
                    posted='-'
                else:
                    posted=tag.find('small',attrs={'data-test':"job-pubilshed-date"}).text
                data['Posted_on'].append(posted)

                #finding skills required for the job
                skill_tag=tag.find('div',attrs={'class':"air3-token-container"})
                skills=skill_tag.find_all('span',attrs={'class':"air3-token"})
                required_skills = []
                for skill in skills:
                    skill_text=skill.text
                    skill_text=skill_text.replace('\n',"").replace(" ",'')
                    required_skills.append(skill_text)
                data['skills_required'].append(required_skills)

                #finding links for job details
                if tag.h2.a['href']==None:
                    links='-'
                else:
                    links=tag.h2.a['href']
                data['job_link'].append(links)

        try:
            directory="C:/Users/SL LAPTOP/PycharmProjects/pythonWebScrapingProject/upwork"
            if not os.path.exists(directory):
                os.makedirs(directory)
            df=pd.DataFrame.from_dict(data)
            file_path = os.path.join(directory,f'upwork_{query}.csv')
            df.to_csv(file_path,index=False)
            print(f"FILE named '{query}.csv' created successfully with {len(data['JOB_title'])} rows")
        except Exception as e:
            print(f'ERROR:{e}')
        time.sleep(5)
        driver.quit()
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
    #checking data after every 1 day
    time.sleep(86400)