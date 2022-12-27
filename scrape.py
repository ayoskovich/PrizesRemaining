from datetime import datetime
import json
import pandas as pd
import boto3

import awswrangler as wr
import sqlalchemy

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
all_data = []
for elem in elems:
    card = PrizeCard(elem.get_attribute("innerHTML"))
    data = card.table_data.assign(game_title=card.title)
    all_data.append(data)

now = str(datetime.now()).replace(":", "-").replace(".", "-")
df = pd.concat(all_data).assign(timestamp=datetime.now())
NAME = f"s3://somethinsbucky/datums/output-{now}.parquet"
print('Shape before processing:', df.shape)
df = proc(df, NAME)
print('Shape after processing:', df.shape)

# Write to s3
wr.s3.to_parquet(df=df, path=NAME)

# Write to db
client = boto3.client('secretsmanager')
response = client.get_secret_value(
    SecretId='rds!db-b98bc80d-69cd-4918-aa32-f0a33add0630'
)['SecretString']

response = json.loads(response)
user, password = response['username'], response['password']
hostname = 'lotto.cvospk6lbhi0.us-east-1.rds.amazonaws.com'
port = 5432
databasename = 'postgres'

cstring = f"postgresql://{user}:{password}@{hostname}:{port}/{databasename}"
eng = sqlalchemy.create_engine(cstring)

with eng.begin() as conn:
    df.to_sql('soldtickets', con=conn, if_exists='append', index=False)

driver.close()
