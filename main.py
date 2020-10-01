import os
from module.utils import Utils
from dotenv import load_dotenv


def main():
    load_dotenv(verbose=True)
    id = os.getenv("NAVER_VIBE_ID")
    pw = os.getenv("NAVER_VIBE_PW")
    utils = Utils()
    driver = utils.get_firefox_driver()
    utils.vibe_login(driver=driver, id=id, pw=pw)


if __name__ == "__main__":
    main()
