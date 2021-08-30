from dataclasses import dataclass, field

from config import CONFIG

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

config = CONFIG()
PLAYLIST_URL_BEGINNING = "https://open.spotify.com/playlist/"

@dataclass
class Song:
    name: str = field()
    artist: str = field()


@dataclass
class Playlist:
    url: str = field()
    name: str = field(default="")
    songs: list = field(default_factory = list, repr=False)

    def check_url_validity(self, url) -> bool:
        return url.startswith(PLAYLIST_URL_BEGINNING)

    def __post_init__(self):
        if self.check_url_validity(self.url):
            print("Valid URL")
        else:
            print("Invalid URL")
            return

p = Playlist("https://open.spotify.com/playlist/23wG5Cdc2rU9DsfTlAg4ij?si=5f84561f1b054c3c")

#s1 = Song("a", "b")
#s2 = Song("b", "b")
#l = [s1]

#print(s2 in l)
