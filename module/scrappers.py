from time import sleep
from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from module.utils import Utils


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
