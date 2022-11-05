from bs4 import BeautifulSoup
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
for elem in elems:
    inner = PrizeCard(elem.get_attribute('innerHTML'))
    print(f"""
        {inner.title=},
        {inner.game_number=},
        {inner.release_date=},
        {inner.price=},
        Data:

        {inner.table_data}
    """)
    print()

driver.close()