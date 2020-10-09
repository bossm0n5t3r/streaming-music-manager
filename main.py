import os
from module.utils import Utils
from module.scrappers import VibeScrapper
from dotenv import load_dotenv


def main():
    load_dotenv(verbose=True)
    id = os.getenv("NAVER_VIBE_ID")
    pw = os.getenv("NAVER_VIBE_PW")
    migrator = VibeScrapper(id=id, pw=pw)
    # migrator.scrap_like()
    # migrator.like("Day Dreaming", "Jack & Jack")
    # migrator.like("Day Dreaming")
    # migrator.add_play_list("test")
    # migrator.add_songs_into_play_list("test", ["Day Dreaming || Jack & Jack", "hello"])
    migrator.scrap_my_play_list(66087627)


if __name__ == "__main__":
    main()
