import os
from module.utils import Utils
from module.scrappers import VibeScrapper
from dotenv import load_dotenv


def main():
    load_dotenv(verbose=True)
    id = os.getenv("NAVER_VIBE_ID")
    pw = os.getenv("NAVER_VIBE_PW")
    migrator = VibeScrapper(id=id, pw=pw)
    migrator.scrap_like()


if __name__ == "__main__":
    main()
