import os
from module.utils import Utils
from module.scrappers import VibeScrapper, MelonScrapper
from dotenv import load_dotenv


def main():
    # load_dotenv(verbose=True)
    # id = os.getenv("NAVER_VIBE_ID")
    # pw = os.getenv("NAVER_VIBE_PW")
    # migrator = VibeScrapper(id=id, pw=pw)
    # migrator.scrap_like()
    # migrator.like("Day Dreaming", "Jack & Jack")
    # migrator.like("Day Dreaming")
    # migrator.add_play_list("test")
    # migrator.add_songs_into_play_list("test", ["Day Dreaming || Jack & Jack", "hello"])
    # migrator.scrap_my_play_list(66087627)
    # migrator.scrap_vibe_play_list("mood_lofi_0001")
    # migrator = MelonScrapper()
    # migrator.scrap_my_play_list(473916599)
    # migrator.scrap_dj_play_list(439646354)
    load_dotenv(verbose=True)
    email = os.getenv("KAKAO_EMAIL")
    pw = os.getenv("KAKAO_PW")
    # utils = Utils()
    # driver = utils.get_firefox_driver()
    # utils.melon_kakao_login(driver=driver, email=email, pw=pw)
    migrator = MelonScrapper(email=email, pw=pw)
    migrator.add_play_list("hello", ["Day Dreaming || Jack & Jack", "hello"])


if __name__ == "__main__":
    main()
