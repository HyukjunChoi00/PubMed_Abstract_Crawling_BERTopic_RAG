#Pubmed Crawling
# 환경변수 - 시스템변수 - Path 에 크롬드라이버 파일을 등록해둘 것

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome()

# URL 입력
# Pubmed는 100 페이지까지만 크롤링 가능
TARGET_URL = "https://pubmed.ncbi.nlm.nih.gov/?term=%28liposome%29+OR+%28lipid+nanoparticle%29&filter=simsearch1.fha&filter=years.2020-2020&size=100&page="
driver.get(TARGET_URL)

# pmid 크롤링
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
id = driver.find_elements(By.CLASS_NAME, "docsum-pmid")
pmid_final = []

last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.5)

    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(1.5)
for i in id:
    k = i.text
    pmid_final.append(k)

# Modify the range
for i in range(2,41) :
    driver.get(TARGET_URL+str(i))
    time.sleep(3)
    id = driver.find_elements(By.CLASS_NAME, "docsum-pmid")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(1.5)

    for i in id:
        k = i.text
        pmid_final.append(k)

# abstract 크롤링
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
TARGET_URL = "https://pubmed.ncbi.nlm.nih.gov/?term=%28liposome%29+OR+%28lipid+nanoparticle%29&filter=simsearch1.fha&filter=years.2020-2020&format=abstract&size=100&page="
driver.get(TARGET_URL)


ab = driver.find_elements(By.CLASS_NAME, "abstract-content.selected")
abstract_final=[]

last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.5)

    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(1.5)
for i in ab:
    abstract = i.text
    abstract_final.append(abstract)

length_of_each = []
for i in range(2,41) :
    driver.get(TARGET_URL+str(i))
    time.sleep(3)
    ab = driver.find_elements(By.CLASS_NAME, "abstract-content.selected")
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(1.5)
    for i in ab:
        abstract = i.text
        abstract_final.append(abstract)
    q1 = len(abstract_final)
    length_of_each.append(q1)

# Make CSV file
import pandas as pd
pub2021=pd.DataFrame({'pmid':pmid_final,'abstract':abstract_final})
pub2021.to_csv('Pubmed_Liposome_2021.csv')
