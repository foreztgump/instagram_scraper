import logging
import datetime
import random

from insta_web_actions import InstaWeb
from time import sleep
from utils import get_correct_path, read_keyword_file

logging.basicConfig(filename='log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    home_path = get_correct_path()
    keyword_list = read_keyword_file(home_path)
    random.shuffle(keyword_list)
    while True:
        count = 0
        rnd_start_time = random.randint(15, 19)
        print(f"Starting at {rnd_start_time} Hour")
        rnd_max_session = random.randint(3, 6)
        print(f"Running {rnd_max_session} Max Sessions")
        for keyword in keyword_list:
            # rnd_max_session_time = random.randint(2, 4)  # hours
            prev_hour = None
            while True:
                d = datetime.datetime.now(datetime.timezone.utc)
                current_hour = d.hour
                if prev_hour is None:
                    prev_hour = d.hour
                    print(f"Current Hour : {d.hour}")
                elif current_hour != prev_hour:
                    print(f"Current Hour : {d.hour}")
                    prev_hour = current_hour

                if d.hour == rnd_start_time:
                    print(f"Start Scraping Keyword : {keyword}")
                    scrape = InstaWeb(keyword)
                    scrape.start()
                    print(f"Scraping Keyword : {keyword} is Done")
                    del scrape
                    break
                else:
                    # print("Sleep For 30 Min")
                    sleep(1800)
            rnd_sleep_time_between_session = random.randint(30, 180) * 60  # minutes
            print(f"Sleep For {rnd_sleep_time_between_session} Min")
            sleep(rnd_sleep_time_between_session)
            count += 1
            if count > rnd_max_session:
                break
