import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

def read_user_credentials(filename):
    # Reading in txt file where we have our user credentials
    with open(filename, 'r',encoding="utf-8") as file:
        user_credentials = [line.rstrip() for line in file.readlines()]
    return user_credentials[0],user_credentials[1]

def linkedin_login(driver):
    # Enter the site
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    # Accept cookies if notification pops up
    try:
        test= "/html/body/div/main/div[1]/div/section/div/div[2]/button[2]"
        driver.find_element(By.XPATH, test).click()
    except:
        print("no cookies notification")
    user_name,password = read_user_credentials('user_credentials.txt')
    driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(user_name)
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(password)
    time.sleep(1)
    # log in
    driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button').click()
    driver.implicitly_wait(20) # wait 20 seconds for webpage to fully load

def job_search(url,driver):
    # click on Jobs button
    driver.find_element(By.XPATH,'//*[@id="global-nav"]/div/nav/ul/li[3]/a').click()
    time.sleep(3)
    # go to search results directly by link
    driver.get(url)
    time.sleep(3)
    
    
driver = webdriver.Chrome()
driver.implicitly_wait(10)
linkedin_login(driver)
QUERY = 'https://www.linkedin.com/jobs/search/?geoId=102454443&keywords=data%20analyst&location=Singapore'
job_search(QUERY,driver)

# collect links for all job offers
links = []
# navigate 6 pages out of the 15 to get 150 results
try: 
    for page in range(1,7):
        time.sleep(2)
        jobs_block = driver.find_element(By.CLASS_NAME,'jobs-search-results-list')
        jobs_list = jobs_block.find_elements(By.CSS_SELECTOR,'.jobs-search-results__list-item')
        for job in jobs_list:
            all_links = job.find_elements(By.TAG_NAME,'a')
            for a in all_links:
                if a.get_attribute('href').startswith("https://www.linkedin.com/jobs/view"): # and a.get_attribute('href') not in links: 
                    links.append(a.get_attribute('href'))
            # scroll down for each job element
            driver.execute_script("arguments[0].scrollIntoView();", job)
        print(f'Collecting the links in the page: Page {page}')
        # go to next page:
        driver.find_element(By.XPATH, f"//button[@aria-label='Page {page + 1}']").click()
        time.sleep(3)
except Exception as err:
    print(f"{type(err).__name__} was raised: {err}")

print(f"number of links = {len(links)}")
job_titles = []
company_names = []
job_desc = []

for i in range(len(links)):
    link = links[i]
    try:
        # go to job offer page
        driver.get(link)
        time.sleep(2)
        # when we get to the job offer page, we need to click on the See More button to access the entire job description.
        driver.find_element(By.CLASS_NAME,"artdeco-card__action").click()
        time.sleep(2)
    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
        continue #issue parsing current link, continue to next one
    # find the general information of the job offers
    try:
        information = driver.find_elements(By.CLASS_NAME,'p5')
        for content in information:
            try:
                job_titles.append(content.find_element(By.CLASS_NAME,"job-details-jobs-unified-top-card__job-title").text)
            except Exception as err:
                print(link)
                job_titles.append("default")
                print(f"{type(err).__name__} was raised: {err}")
            try:
                #company_names.append(content.find_element(By.CLASS_NAME,"job-details-jobs-unified-top-card__primary-description").find_element(By.TAG_NAME,'a').text)
                company_names.append(content.find_element(By.CLASS_NAME,"job-details-jobs-unified-top-card__primary-description").text)
            except Exception as err:
                print(link)
                company_names.append("default")
                print(f"{type(err).__name__} was raised: {err}")
                
            time.sleep(2)
    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
    try:
        # get job description
        job_description = driver.find_elements(By.CLASS_NAME,'jobs-description__content')
        for description in job_description:
            job_text = description.find_element(By.CLASS_NAME,"jobs-box__html-content").text
            job_desc.append(job_text)
            time.sleep(2)
    except Exception as err:
        print(link)
        job_desc.append("default")
        print(f"{type(err).__name__} was raised: {err}")
    print(f"link {i + 1} is processed, job_desc_length = {len(job_desc)}, job_titles_length = {len(job_titles)}, company_lengths = {len(company_names)}")

# Creating the dataframe 
df = pd.DataFrame(list(zip(job_titles,company_names,job_desc)), columns =['job_title', 'company_name','job_desc'])

# Storing the data to csv file
df.to_csv('../data/job_offers.csv', index=False)
                                            
print("Ended")
                                            
# close webdriver
driver.quit()

