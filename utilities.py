from dataclasses import dataclass
from bs4 import BeautifulSoup
import pandas as pd
import html5lib


@dataclass
class PrizeCard:
    """Wraps the html text of a prize card."""

    _html: str

    @property
    def bs(self):
        """Beautiful soup representation"""
        return BeautifulSoup(self._html, features="html5lib")

    @property
    def details_link(self):
        el = self.bs.find('div', class_='prizes-remaining-card-image').find('a')
        return el['href']

    @property
    def title(self):
        return self.bs.find("p", class_="game-title").text

    @property
    def game_number(self):
        return self.bs.find("p", class_="game-number").text

    @property
    def price(self):
        return self.bs.find("p", class_="game-price").text

    @property
    def release_date(self):
        return self.bs.find("p", class_="game-release-date").text

    @property
    def table_data(self) -> pd.DataFrame:
        tab = self.bs.find("div", class_="prizes-remaining-card-table")
        dat = pd.read_html(tab.encode_contents(), flavor="bs4")[0]
        # TODO: clean up column types, remove "TOTAL:" rows
        return dat


def remove_totals(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[lambda x: x["PRIZE"] != "TOTAL:"]

def convert_gamenumber(gamenumber: str) -> int:
    return pd.to_numeric(gamenumber.replace('Game Number: ', ''))

def convert_price(price: str) -> int:
    return pd.to_numeric(price.replace(' ', '').replace('Price:$', ''))

def convert_release_date(rd: str) -> str:
    return pd.to_datetime(rd.replace('Release Date: ', ''), format='%b %d, %Y')

def convert_prize(prize: str) -> int:
    """Converts the prize column.

    $50 -> 50
    $3,000 -> 3000
    """
    return pd.to_numeric(prize.replace("$", "").replace(",", ""))


def proc(df: pd.DataFrame, fname: str) -> pd.DataFrame:
    """Processing pipeline for an individual file"""
    rv = (
        df.pipe(remove_totals)
        .assign(PRIZE=lambda x: x["PRIZE"].apply(convert_prize), src=fname)
        .assign(game_number = lambda x: x['game_number'].apply(convert_gamenumber))
        .assign(price = lambda x: x['price'].apply(convert_price))
        .assign(release_date = lambda x: x['release_date'].apply(convert_release_date))
        .rename(
            columns={
                "PRIZE": "prize_amount",
                "REMAINING": "prizes_remaining",
                "START": "prizes_start",
                "game_title": "game_title",
                "timestamp": "timestamp",
                "src": "s3_source",
            },
            errors="raise",
        )
    )
    return rv
