from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from config import CONFIG
from playlist import Playlist, Song
from constants import PLAYLIST_LENGTH_XPATH, PLAYLIST_NAME_XPATH, SONGS_LIST_XPATH
from tqdm import tqdm

class Inteface:
    def __init__(self):
        config = CONFIG()
        options = webdriver.ChromeOptions()
        options.binary_location = config.BINARY_PATH
        if config.HEADLESS:
            options.add_argument('headless')

        print("Setting up driver...")
        self.driver = webdriver.Chrome(executable_path = config.DRIVER_PATH, options=options)
        print("Done!")
        self.current_playlist = None

    def wait_for_element(self, by, locator):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, locator)))
        finally:
            return element

    def get_playlist_songs(self):
        songs = []

        html = self.driver.find_element_by_tag_name('html')
        html.click()

        pbar = tqdm(total=self.current_playlist.length, bar_format='{l_bar}{bar:50}{r_bar}{bar:-10b}')
        while len(songs) < self.current_playlist.length:
            songs_list = self.wait_for_element(By.XPATH, SONGS_LIST_XPATH)

            song_index = 1
            while True:
                try:
                    try:
                        row = songs_list.find_element_by_xpath(SONGS_LIST_XPATH + f"/div[{song_index}]")
                        song_name = row.find_element_by_class_name("_gvEBguxvbSruOQCkWrz").text
                        artist_name = row.find_element_by_class_name("lm4ptx0mVHQ1OEgJR6R5").text
                    except StaleElementReferenceException:
                        continue

                    song = Song(song_name, artist_name)
                    if song not in songs:
                        songs.append(song)
                        pbar.update(1)
                except NoSuchElementException:
                    break
                song_index += 1

            #print("songs in list:", len(songs))

            for _ in range(20):
                html.send_keys(Keys.DOWN)

        self.current_playlist.songs = songs
        pbar.close()


    def set_playlist(self, url):
        if not Playlist.check_url_validity(url):
            raise Exception("Invalid playlist URL")

        print("Setting url to playlist url... ", end="")
        self.driver.get(url)
        print(f"[url: {url}]")
        name, length = self.get_playlist_data()
        self.current_playlist = Playlist(url, name, length)

        print("Fetching playlist songs")
        self.get_playlist_songs()
        print("Done!")

        #for idx, song in enumerate(self.current_playlist.songs):
            #print(idx+1, song)


    def get_playlist_data(self):
        print("Fetching playlist name... ", end="")
        playlist_name = self.wait_for_element(By.XPATH, PLAYLIST_NAME_XPATH).get_attribute("innerText")
        print(f"[name: {playlist_name}]")
        print("Fetching playlist length... ", end="")
        playlist_length = int(self.wait_for_element(By.XPATH, PLAYLIST_LENGTH_XPATH).get_attribute("innerHTML").split("songs")[0])
        print(f"[length: {playlist_length}]")

        return playlist_name, playlist_length


    def quit(self):
        self.driver.close()
        self.driver.quit()


playlist_url = "https://open.spotify.com/playlist/6a1vCLOZaXcK7iiT0SOa6r?si=a1b641aa04ae4319"
i = Inteface()
i.set_playlist(playlist_url)
i.quit()
