from dataclasses import dataclass
from bs4 import BeautifulSoup

@dataclass
class PrizeCard:
    """ Wraps the html text of a prize card. """
    _html: str

    @property
    def bs(self):
        """ Beautiful soup representation """
        return BeautifulSoup(self._html)
    
    @property
    def title(self):
        return self.bs.find('p', class_='game-title').text

    @property
    def game_number(self):
        return self.bs.find('p', class_='game-number').text

    @property
    def price(self):
        return self.bs.find('p', class_='game-price').text

    @property
    def release_date(self):
        return self.bs.find('p', class_='game-title').text

    @property
    def table_data(self):
        pass