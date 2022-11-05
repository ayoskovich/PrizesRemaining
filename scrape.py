from bs4 import BeautifulSoup
import pandas as pd 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from utilies import PrizeCard

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')

service = Service(executable_path='/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=opts)
driver.get("https://www.michiganlottery.com/resources/instant-games-prizes-remaining")
elems = driver.find_elements(By.CLASS_NAME, "prizes-remaining-card")

print(f'{len(elems)} cards found.')
all_data = []
for elem in elems:
    card = PrizeCard(elem.get_attribute('innerHTML'))
    data = card.table_data.assign(game_title = card.title)
    all_data.append(data)

print(pd.concat(all_data))
driver.close()