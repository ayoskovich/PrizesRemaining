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
        return self.bs.find("p", class_="game-title").text

    @property
    def table_data(self) -> pd.DataFrame:
        tab = self.bs.find("div", class_="prizes-remaining-card-table")
        dat = pd.read_html(tab.encode_contents(), flavor="bs4")[0]
        # TODO: clean up column types, remove "TOTAL:" rows
        return dat
