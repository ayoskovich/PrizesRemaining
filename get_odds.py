"""
This script is meant to be run locally, inside a Docker container.

It scrapes the lotto page and saves the odds into a database.

It could probably somehow be sped up.
"""
from datetime import datetime
import json

import pandas as pd
import boto3
import awswrangler as wr
import sqlalchemy
from sqlalchemy import text

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from utilities import PrizeCard, proc

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=opts)
driver.get("https://www.michiganlottery.com/resources/instant-games-prizes-remaining")
elems = driver.find_elements(By.CLASS_NAME, "prizes-remaining-card")

print(f"{len(elems)} cards found.")

# Get the first page of data
all_data = []
all_cards = []
for elem in elems:
    card = PrizeCard(elem.get_attribute("innerHTML"))
    all_cards.append(card)
    data = card.table_data.assign(
        game_title=card.title,
        game_number=card.game_number,
        price=card.price,
        release_date=card.release_date,
        details_link=card.details_link
    )
    all_data.append(data)

def parse_game_number(gn: str) -> int:
    """
    Game Number: 464 -> 464
    """
    return int(
        gn
        .replace(' ', '')
        .replace('GameNumber:', '')
    )

def parse_odds(odds: str):
    """
    Overall Odds: 1 in 3.10 -> 1, 3.10
    """
    x = odds.split(':')[1]
    num, den = x.split('in')
    return float(num), float(den)

NOW = datetime.now()

odddata = []
for card in all_cards:
    link = f'https://www.michiganlottery.com{card.details_link}'
    try:
        driver.get(link)
        title = driver.find_element(By.ID, 'landing-title')
        elem = driver.find_element(By.CLASS_NAME, 'game-info-odds')
        print(f'Odds are: {elem.text} for {card.game_number}')
        num, den = parse_odds(elem.text)
        odddata.append({
            'game_number': parse_game_number(card.game_number), 
            'num': num, 'den': den,
            'run_date': NOW
        })
    except Exception as e:
        print(f'There was an issue finding the link for {link}. ({e})')

client = boto3.client("secretsmanager", region_name='us-east-1')
response = client.get_secret_value(
    SecretId="rds!db-b98bc80d-69cd-4918-aa32-f0a33add0630"
)["SecretString"]

response = json.loads(response)
user, password = response["username"], response["password"]
hostname = "lotto.cvospk6lbhi0.us-east-1.rds.amazonaws.com"
port = 5432
databasename = "postgres"

cstring = f"postgresql://{user}:{password}@{hostname}:{port}/{databasename}"
eng = sqlalchemy.create_engine(cstring)

with eng.begin() as conn:
    for row in odddata:
        conn.execute(text("""
        INSERT INTO odds
        (game_number, num, den, run_date)
        VALUES (:game_number, :num, :den, :run_date)
        """), row)