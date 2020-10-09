from time import sleep
from urllib.parse import quote
from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from module.utils import Utils
import pyperclip


class Scrapper(metaclass=ABCMeta):
    def __init__(self, id=None, pw=None):
        self.utils = Utils()
        # self.chrome_driver = self.utils.get_chrome_driver()
        self.firefox_driver = self.utils.get_firefox_driver()
        self.id = id
        self.pw = pw


class VibeScrapper(Scrapper):
    def find_btn_more_list(self):
        isFound = True
        while isFound:
            try:
                self.firefox_driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                sleep(1)
                self.firefox_driver.find_element_by_class_name("btn_more_list").click()
                sleep(3)
            except:
                print("There is no more btn_more_list button")
                isFound = False

    def scrap_like(self):
        try:
            isVibeLoginSuccess = self.utils.vibe_login(
                driver=self.firefox_driver, id=self.id, pw=self.pw
            )
            if isVibeLoginSuccess:
                print("scrap all like songs")
                link = "https://vibe.naver.com/library/tracks"
                self.firefox_driver.get(link)
                sleep(3)
                self.find_btn_more_list()
                soup = BeautifulSoup(self.firefox_driver.page_source, "html.parser")
                title = soup.select(
                    "#content > div > div.track_section > div > div > table > tbody > tr > td.song > div.title_badge_wrap > span > a"
                )
                singer = soup.select(
                    "#content > div > div.track_section > div > div > table > tbody > tr > td.artist"
                )
                play_list = []
                for i in range(len(title)):
                    play_list.append([title[i].text, singer[i]["title"]])
                with open("VIBE_Playlist.txt", "w", encoding="utf-8") as f:
                    for item in play_list:
                        song, singer = item
                        f.write("%s || %s\n" % (song, singer))
                f.close()
                print("Scrap VIBE like songs Successed")
        except:
            print("Failed to scrap VIBE Playlist")
        finally:
            self.utils.shutdown(
                msg="VibeScrapper is closed", driver=self.firefox_driver
            )

    def generate_url_safe_search_keyword(self, song, singer):
        keyword = ""
        if singer is None:
            keyword = song
        else:
            keyword = song + " - " + singer
        return quote(keyword)

    def click_like(self):
        self.firefox_driver.find_element_by_css_selector(
            "#content > div:nth-child(2) > div > div:nth-child(2) > div.option"
        ).click()
        sleep(1)
        self.firefox_driver.find_element_by_css_selector(
            "#content > div:nth-child(2) > div > div:nth-child(2) > div.option > div > div > div > a:nth-child(2)"
        ).click()
        sleep(1)

    def like(self, song, singer=None):
        try:
            isVibeLoginSuccess = self.utils.vibe_login(
                driver=self.firefox_driver, id=self.id, pw=self.pw
            )
            if isVibeLoginSuccess:
                print("add song into like list")
                url_safe_search_keyword = self.generate_url_safe_search_keyword(
                    song, singer
                )
                self.firefox_driver.get(
                    "https://vibe.naver.com/search?query=" + url_safe_search_keyword
                )
                self.click_like()
                print("Add song into like list Successed")
        except:
            print("Failed to add song into like list")
        finally:
            self.utils.shutdown(
                msg="VibeScrapper is closed", driver=self.firefox_driver
            )

    def add_play_list(self, play_list_name):
        try:
            isVibeLoginSuccess = self.utils.vibe_login(
                driver=self.firefox_driver, id=self.id, pw=self.pw
            )
            if isVibeLoginSuccess:
                print("Add new play list")
                self.firefox_driver.get("https://vibe.naver.com/library/playlists")
                add_item_element = self.firefox_driver.find_element_by_class_name(
                    "btn_add_item"
                )
                add_item_element.click()
                sleep(1)
                input_playlist_element = self.firefox_driver.find_element_by_class_name(
                    "input_playlist"
                )
                input_playlist_element.click()
                pyperclip.copy(play_list_name)
                input_playlist_element.send_keys(Keys.COMMAND, "v")
                sleep(1)
                self.firefox_driver.find_element_by_css_selector(
                    "#app > div.modal > div > div > div > a.point"
                ).click()
                sleep(1)
                print("Add new play list Successed")
        except:
            print("Failed to add new play list")
        finally:
            self.utils.shutdown(
                msg="VibeScrapper is closed", driver=self.firefox_driver
            )
