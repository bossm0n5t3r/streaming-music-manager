from time import sleep
from urllib.parse import quote
from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from module.utils import Utils
import pyperclip


class Scrapper(metaclass=ABCMeta):
    def __init__(self, email=None, id=None, pw=None):
        self.utils = Utils()
        # self.chrome_driver = self.utils.get_chrome_driver()
        self.firefox_driver = self.utils.get_firefox_driver()
        self.email = email
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

    def get_song_and_singer_from_like(self):
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
        return play_list

    def get_song_and_singer_from_play_list(self):
        soup = BeautifulSoup(self.firefox_driver.page_source, "html.parser")
        title = soup.select(
            "#content > div.track_section > div > div > table > tbody > tr > td.song > div.title_badge_wrap > span > a"
        )
        singer = soup.select(
            "#content > div.track_section > div > div > table > tbody > tr > td.artist"
        )
        play_list = []
        for i in range(len(title)):
            play_list.append([title[i].text, singer[i]["title"]])
        return play_list

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
                play_list = self.get_song_and_singer_from_like()
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

    def generate_url_safe_search_keyword(self, song, singer=None):
        keyword = ""
        if singer is None:
            keyword = song
        else:
            keyword = song + " - " + singer
        return quote(keyword)

    def find_song(self, url_safe_search_keyword):
        self.firefox_driver.get(
            "https://vibe.naver.com/search?query=" + url_safe_search_keyword
        )

    def click_song_option(self):
        self.firefox_driver.find_element_by_css_selector(
            "#content > div:nth-child(2) > div > div:nth-child(2) > div.option"
        ).click()
        sleep(1)

    def click_song_option_like(self):
        self.firefox_driver.find_element_by_css_selector(
            "#content > div:nth-child(2) > div > div:nth-child(2) > div.option > div > div > div > a:nth-child(2)"
        ).click()
        sleep(1)

    def click_song_option_add_play_list(self, play_list_name):
        self.firefox_driver.find_element_by_css_selector(
            "#content > div:nth-child(2) > div > div:nth-child(2) > div.option > div > div > div > a:nth-child(3)"
        ).click()
        sleep(1)
        self.firefox_driver.find_element_by_xpath(
            '//em[@class="ly_playlist_title" and text()="' + play_list_name + '"]'
        ).click()
        sleep(1)
        self.firefox_driver.find_element_by_css_selector(
            "#app > div.modal > div > div > div > a"
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
                self.find_song(url_safe_search_keyword)
                self.click_song_option()
                self.click_song_option_like()
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

    def get_all_play_list_title_list(self):
        self.firefox_driver.get("https://vibe.naver.com/library/playlists")
        sleep(1)
        soup = BeautifulSoup(self.firefox_driver.page_source, "html.parser")
        play_list_title_list_data = soup.select(
            "#content > div > div.sub_list > ul > li > div > div.info > a > span.text"
        )
        play_list_title_list = []
        for i in range(len(play_list_title_list_data)):
            play_list_title_list.append(play_list_title_list_data[i].text)
        return play_list_title_list

    def add_songs_into_play_list(self, play_list_name, song_datas):
        # 노래 리스트로 받을 경우, 파일 경로 X
        try:
            # 로그인
            isVibeLoginSuccess = self.utils.vibe_login(
                driver=self.firefox_driver, id=self.id, pw=self.pw
            )
            if isVibeLoginSuccess:
                print("add songs into play list")
                # play_list_name으로 play_list 찾기
                all_play_list_titles = self.get_all_play_list_title_list()
                # 없으면 생성
                if play_list_name not in all_play_list_titles:
                    self.add_play_list(play_list_name)
                sleep(1)
                for song_data in song_datas:
                    # 각 노래마다 검색
                    song, singer = None, None
                    if song_data.find("||") != -1:
                        song, singer = [
                            x.strip() for x in list(map(str, song_data.split("||")))
                        ]
                    else:
                        song = song_data
                    url_safe_search_keyword = self.generate_url_safe_search_keyword(
                        song, singer
                    )
                    self.find_song(url_safe_search_keyword)

                    # 각 노래마다 play_list에 추가하기
                    self.click_song_option()
                    self.click_song_option_add_play_list(play_list_name)
                print("Add songs into play list Successed")
        except:
            print("Failed to add songs into play list")
        finally:
            self.utils.shutdown(
                msg="VibeScrapper is closed", driver=self.firefox_driver
            )

    def scrap_my_play_list(self, my_play_list_number):
        try:
            isVibeLoginSuccess = self.utils.vibe_login(
                driver=self.firefox_driver, id=self.id, pw=self.pw
            )
            if isVibeLoginSuccess:
                print("scrap my play list songs")
                link = "https://vibe.naver.com/mylist/" + str(my_play_list_number)
                self.firefox_driver.get(link)
                sleep(3)
                self.find_btn_more_list()
                play_list = self.get_song_and_singer_from_play_list()
                with open(
                    "VIBE_" + str(my_play_list_number) + "_Playlist.txt",
                    "w",
                    encoding="utf-8",
                ) as f:
                    for item in play_list:
                        song, singer = item
                        f.write("%s || %s\n" % (song, singer))
                f.close()
                print("Scrap my play list songs Successed")
        except:
            print("Failed to scrap my play list songs")
        finally:
            self.utils.shutdown(
                msg="VibeScrapper is closed", driver=self.firefox_driver
            )

    def scrap_vibe_play_list(self, play_list_name):
        try:
            isVibeLoginSuccess = self.utils.vibe_login(
                driver=self.firefox_driver, id=self.id, pw=self.pw
            )
            if isVibeLoginSuccess:
                print("scrap vibe play list songs")
                link = "https://vibe.naver.com/playlist/" + play_list_name
                self.firefox_driver.get(link)
                sleep(3)
                self.find_btn_more_list()
                play_list = self.get_song_and_singer_from_play_list()
                with open(
                    "VIBE_" + play_list_name + "_Playlist.txt",
                    "w",
                    encoding="utf-8",
                ) as f:
                    for item in play_list:
                        song, singer = item
                        f.write("%s || %s\n" % (song, singer))
                f.close()
                print("Scrap vibe play list songs Successed")
        except:
            print("Failed to scrap vibe play list songs")
        finally:
            self.utils.shutdown(
                msg="VibeScrapper is closed", driver=self.firefox_driver
            )


class MelonScrapper(Scrapper):
    def scrap_my_page(self, page=None):
        if page is not None:
            self.firefox_driver.execute_script(
                "javascript:pageObj.sendPage('" + str(page * 50 + 1) + "')"
            )
        soup = BeautifulSoup(self.firefox_driver.page_source, "html.parser")
        title = soup.select(
            "#frm > div > table > tbody > tr > td:nth-child(3) > div > div > a.fc_gray"
        )
        singer = soup.select("#artistName > a")
        plist = []
        for i in range(len(title)):
            plist.append(title[i].text + " || " + singer[i].text)
        return plist

    def scrap_my_play_list(self, plylstSeq):
        try:
            link = (
                "https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq="
                + str(plylstSeq)
            )
            self.firefox_driver.get(link)
            sleep(1)
            max_page = [
                int(x)
                for x in self.firefox_driver.find_element_by_class_name("page_num").text
            ]
            plist = []
            for page_num in max_page:
                plist += self.scrap_my_page(page_num)
            with open(
                "Melon_" + str(plylstSeq) + "_Playlist.txt", "w", encoding="utf-8"
            ) as f:
                for data in plist:
                    f.write("%s\n" % data)
            f.close()
            print("Scrap Melon My Playlist Successed")
        except:
            print("Failed to scrap Melon My Playlist")
        finally:
            self.utils.shutdown(
                msg="MelonScrapper is closed", driver=self.firefox_driver
            )

    def scrap_dj_page(self, page=None):
        if page is not None:
            self.firefox_driver.execute_script(
                "javascript:pageObj.sendPage('" + str(page * 50 + 1) + "')"
            )
        soup = BeautifulSoup(self.firefox_driver.page_source, "html.parser")
        title = soup.select(
            "#frm > div > table > tbody > tr > td:nth-child(5) > div > div > div.ellipsis.rank01 > span > a"
        )
        singer = soup.select(
            "#frm > div > table > tbody > tr > td:nth-child(5) > div > div > div.ellipsis.rank02 > a"
        )
        plist = []
        for i in range(len(title)):
            plist.append(title[i].text + " || " + singer[i].text)
        return plist

    def scrap_dj_play_list(self, plylstSeq):
        try:
            link = (
                "https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq="
                + str(plylstSeq)
            )
            self.firefox_driver.get(link)
            sleep(1)
            max_page = [
                int(x)
                for x in self.firefox_driver.find_element_by_class_name("page_num").text
            ]
            plist = []
            for page_num in max_page:
                plist += self.scrap_dj_page(page_num)
            with open(
                "Melon_" + str(plylstSeq) + "_DJ_Playlist.txt", "w", encoding="utf-8"
            ) as f:
                for data in plist:
                    f.write("%s\n" % data)
            f.close()
            print("Scrap Melon Dj Playlist Successed")
        except:
            print("Failed to scrap Melon Dj Playlist")
        finally:
            self.utils.shutdown(
                msg="MelonScrapper is closed", driver=self.firefox_driver
            )

    def search_keyword(self, song, singer=None):
        keyword = ""
        if singer is None:
            keyword = song
        else:
            keyword = song + " - " + singer
        return keyword

    def add_play_list(self, play_list_name, song_datas):
        try:
            isMelonLoginSuccess = self.utils.melon_kakao_login(
                driver=self.firefox_driver, email=self.email, pw=self.pw
            )
            if isMelonLoginSuccess:
                print("Add new play list")
                self.firefox_driver.get(
                    "https://www.melon.com/mymusic/playlist/mymusicplaylistinsert_insert.htm"
                )
                self.firefox_driver.find_element_by_id("title").send_keys(
                    play_list_name
                )
                sleep(1)
                self.firefox_driver.find_element_by_xpath(
                    '//span[text()="곡 검색"]'
                ).click()
                sleep(1)
                d_kwd_element = self.firefox_driver.find_element_by_id("d_kwd")
                for song_data in song_datas:
                    # 각 노래마다 검색
                    song, singer = None, None
                    if song_data.find("||") != -1:
                        song, singer = [
                            x.strip() for x in list(map(str, song_data.split("||")))
                        ]
                    else:
                        song = song_data
                    keyword = self.search_keyword(song, singer)
                    d_kwd_element.clear()
                    sleep(1)
                    d_kwd_element.send_keys(keyword)
                    sleep(1)
                    d_kwd_element.send_keys(Keys.RETURN)
                    sleep(1)
                    self.firefox_driver.find_element_by_css_selector(
                        "#conts > div > div > div > div.music_list > div > ul > li.tab05_3.on > div > div.song_list.d_scrolldiv > table > tbody > tr > td.t_center > div > input"
                    ).click()
                    sleep(1)
                    self.firefox_driver.find_element_by_class_name("move_right").click()
                    sleep(1)
                self.firefox_driver.find_element_by_class_name("btn_green_h30").click()
                sleep(1)
                Alert(self.firefox_driver).accept()
                sleep(1)
                print("Add new play list Successed")
        except:
            print("Failed to add new play list")
        finally:
            self.utils.shutdown(
                msg="MelonScrapper is closed", driver=self.firefox_driver
            )
