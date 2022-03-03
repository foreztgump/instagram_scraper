import os
import json
import random
import logging
import subprocess
import undetected_chromedriver as uc

from time import sleep
from bs4 import BeautifulSoup
from os.path import expanduser

from constants import GLOBAL_CHROME, GLOBAL_CHROME_PROFILE_PATH

from utils import type_me, get_correct_path, proper_round, write_to_file

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

logging.basicConfig(filename='log', filemode='a', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class InstaWeb(object):
    def __init__(self, keyword):
        self.abs_path = get_correct_path()
        self.keyword = keyword
        # ----------------------------------------- Init Variable ------------------------------------------------------

        self.agree_api_app = '/html/body/div/div[2]/div/div/div[4]/div/form/button'

        self.search_box = '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[1]/div/span[2]'

        # --------------------------------------- Configure Browser ----------------------------------------------------
        process = subprocess.Popen(
            ['reg', 'query', f'{GLOBAL_CHROME}', '/v', 'version'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )
        version = process.communicate()[0].decode('UTF-8').strip().split()[-1]
        major_version = version.split('.')[0]
        uc.TARGET_VERSION = major_version
        uc.install()

        brave = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
        # Extensions Path
        # path = f"{self.abs_path}/extensions/fjkmabmdepjfammlpliljpnbhleegehm"
        # path2 = f"{self.abs_path}/extensions/pcboajngloecgmaailkmphmpbacmbcfb"

        home_path = expanduser("~")
        profile_path = os.path.join(home_path + GLOBAL_CHROME_PROFILE_PATH)

        options = webdriver.ChromeOptions()
        options.add_argument(f'user-data-dir={profile_path}')
        options.add_argument("--profile-directory=Profile 2")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-web-security")
        viewport = ['1366,768']  # '1920,1080',
        options.add_argument(f"--window-size={random.choice(viewport)}")
        options.add_argument("--log-level=3")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        # options.add_argument(f'--load-extension={path}')
        options.binary_location = chrome
        self.driver = uc.Chrome(options=options)

    def start(self):
        with self.driver:
            self.driver.implicitly_wait(5)
            sleep_rnd = random.randint(2, 30)
            user_list = []
            chance_to_browse = random.randint(1, 2)
            if chance_to_browse == 1:
                self.browse()
            if '#' in self.keyword:
                try:
                    chance_to_browse = random.randint(1, 4)
                    if chance_to_browse == 1:
                        self.browse()

                    logger.info('Getting User List From Hashtag')
                    user_list = self.get_users_links_from_hashtag_page(self.keyword)

                    chance_to_browse = random.randint(1, 4)
                    if chance_to_browse == 1:
                        self.browse()

                except Exception as e:
                    logger.info(f'Failed Getting User List : {e}')

                if len(user_list) > 0:
                    print(f"Found {len(user_list)} Users to Scrape")
                    user_to_file = []
                    for user in user_list:
                        try:
                            chance_to_browse = random.randint(1, 5)
                            if chance_to_browse == 1:
                                self.browse()
                            logger.info('Getting Post List from User Hashtag List')
                            post_list = self.get_user_post_links_soup(user)
                            if len(post_list) > 0:
                                print(f"Found {len(post_list)} Posts to Scrape")
                                for post in post_list:
                                    try:
                                        chance_to_browse = random.randint(1, 6)
                                        if chance_to_browse == 1:
                                            self.browse()
                                        logger.info('Getting Liked By User List from Hashtag List')
                                        user_list_extend = self.get_liked_by_user_soup(post)
                                        if len(user_list_extend) > 0:
                                            user_to_file.extend(user_list_extend)
                                            print(f"Found {len(user_to_file)} Users From Posts to Save So Far")
                                        sleep(sleep_rnd)
                                    except Exception as e:
                                        logger.info(f'Failed Getting Post Liked By User List from Hashtag : {e}')
                            sleep(sleep_rnd)
                        except Exception as e:
                            logger.info(f'Failed Getting Post List From User : {e}')
                    write_to_file(line_list=user_to_file, home_path=self.abs_path)

            else:
                chance_to_browse = random.randint(1, 4)
                if chance_to_browse == 1:
                    self.browse()
                user_list = self.parse_search_box(self.keyword)
                if len(user_list) > 0:
                    print(f"Found {len(user_list)} Users to Scrape")
                    user_to_file = []
                    for user in user_list:
                        try:
                            chance_to_browse = random.randint(1, 5)
                            if chance_to_browse == 1:
                                self.browse()
                            logger.info('Getting Post List from User Hashtag List')
                            post_list = self.get_user_post_links_soup(user)
                            if len(post_list) > 0:
                                print(f"Found {len(post_list)} Posts to Scrape")
                                for post in post_list:
                                    try:
                                        chance_to_browse = random.randint(1, 6)
                                        if chance_to_browse == 1:
                                            self.browse()
                                        logger.info('Getting Liked By User List from Hashtag List')
                                        user_list_extend = self.get_liked_by_user_soup(post)
                                        if len(user_list_extend) > 0:
                                            user_to_file.extend(user_list_extend)
                                            print(f"Found {len(user_to_file)} Users From Posts to Save So Far")
                                        sleep(sleep_rnd)
                                    except Exception as e:
                                        logger.info(f'Failed Getting Post Liked By User List from Hashtag : {e}')
                            sleep(sleep_rnd)
                        except Exception as e:
                            logger.info(f'Failed Getting Post List From User : {e}')
                write_to_file(line_list=user_to_file, home_path=self.abs_path)

            self.driver.close()

    def browse(self):
        explore_url = 'https://www.instagram.com/explore/'
        home_url = 'https://www.instagram.com/'
        logger.info('- Start Browsing -')
        print('Start Browsing')

        chance_to_browse_choose = random.randint(1, 2)
        rnd_times_to_browse = random.randint(1, 30)
        # Browse Explore
        if chance_to_browse_choose == 1:
            try:
                logger.info('- Browsing Explore -')
                print("Browsing Explore")
                self.driver.get(explore_url)
                for i in range(0, rnd_times_to_browse):
                    posts = []
                    try:
                        links = self.driver.find_elements(By.TAG_NAME, 'a')
                        # print(links)
                        for link in links:
                            post = link.get_attribute('href')
                            # print(post)
                            if '/p/' in post:
                                posts.append(link)
                    except:
                        logger.exception('!- Failed Getting Post Links -')
                        print('Failed Getting Post Links')

                    try:
                        pause_time = random.uniform(2, 8)
                        sleep(pause_time)
                        chance_to_watch_post = random.randint(1, 5)
                        if chance_to_watch_post == 1:
                            chose = random.randint(0, len(posts))
                            action = ActionChains(self.driver)
                            action.move_to_element(posts[chose]).click().perform()
                            pause_time = random.uniform(5, 20)
                            sleep(pause_time)

                            close = self.driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Close']")
                            action.move_to_element(close).click().perform()
                        else:
                            rnd_scroll = random.randint(20, 250)
                            rnd_speed = random.randint(2, 20)
                            self.scroll_down_page(times=rnd_scroll, speed=rnd_speed)
                            scroll_pause_time = random.uniform(1, 5)
                            sleep(scroll_pause_time)

                        chance_to_scroll = random.randint(1, 4)
                        if chance_to_scroll == 1:
                            pause_time = random.uniform(3, 8)
                            sleep(pause_time)
                            rnd_scroll = random.randint(20, 250)
                            rnd_speed = random.randint(2, 20)
                            self.scroll_down_page(times=rnd_scroll, speed=rnd_speed)

                        chance_to_scroll_up = random.randint(1, 6)
                        if chance_to_scroll_up == 1:
                            for i in range(0, 5):
                                self.page_up()
                    except:
                        logger.info('- Scroll to Find Post Links -')
                        rnd_scroll = random.randint(20, 450)
                        rnd_speed = random.randint(2, 20)
                        self.scroll_down_page(times=rnd_scroll, speed=rnd_speed)
                        scroll_pause_time = random.uniform(1, 5)
                        sleep(scroll_pause_time)
            except Exception as e:
                print("Failed Trying to Browse Explore")
                logger.exception(f'!- Failed Trying to Browse Explore - Error : {e} - ')
        # Browse Home
        else:
            try:
                # Scroll Random + Watching Video
                self.driver.get(home_url)
                logger.info('- Browsing Home -')
                print("Browsing Home")
                for i in range(0, (rnd_times_to_browse * 2)):
                    rnd_scroll = random.randint(20, 600)
                    rnd_speed = random.randint(2, 20)
                    self.scroll_down_page(times=rnd_scroll, speed=rnd_speed)
                    scroll_pause_time = random.uniform(1, 5)
                    sleep(scroll_pause_time)
                    watch_chance = random.randint(1, 4)
                    if watch_chance == 1:
                        try:
                            list = self.driver.find_elements(By.CSS_SELECTOR, "span[aria-label='Play']")
                            chose = random.randint(0, len(list))
                            action = ActionChains(self.driver)
                            action.move_to_element(list[chose]).click().perform()
                            watch_pause_time = random.uniform(5, 30)
                            sleep(watch_pause_time)
                        except Exception as e:
                            # print(e)
                            print("cannot find")

                    chance_to_scroll_up = random.randint(1, 6)
                    if chance_to_scroll_up == 1:
                        for i in range(0, 5):
                            self.page_up()
            except Exception as e:
                print("Failed Trying to Browse Home")
                logger.exception(f'!- Failed Trying to Browse Home - Error : {e} - ')

    def scroll_down_page(self, times, speed):
        count = 0
        current_scroll_position = self.driver.execute_script("return document.documentElement.scrollTop")
        while True:
            current_scroll_position += speed
            self.driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            count += 1
            if count > times:
                break

    def page_down(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.PAGE_DOWN)
        action.perform()
        scroll_pause_time = random.uniform(0.25, 1.0)
        sleep(scroll_pause_time)

    def page_up(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.PAGE_UP)
        action.perform()
        scroll_pause_time = random.uniform(0.25, 1.5)
        sleep(scroll_pause_time)

    def rnd_scroll(self):

        scroll_pause_time = random.randint(3, 8)
        scroll_count = random.randint(10, 30)
        scroll_times = random.randint(1, 8)
        pct_rnd = random.randint(10, 50)

        for i in range(0, scroll_times):
            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            print(last_height)
            scroll_for_cal = (last_height * pct_rnd) / 100
            scroll_for = proper_round(scroll_for_cal)
            print(scroll_for_cal)
            print(scroll_for)
            self.driver.execute_script(f"window.scrollTo(0, {scroll_for});")
            scroll_pause_time = random.randint(3, 8)
            sleep(scroll_pause_time)

        # while True:
        #     # Scroll down to bottom
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #
        #     sleep(scroll_pause_time)
        #
        #     # Calculate new scroll height and compare with last scroll height
        #     new_height = self.driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break
        #     elif scroll_count < count:
        #         break
        #     last_height = new_height
        #     count += 1

    def get_user_post_links(self):
        # Parse Post Links From User's Page
        posts = []
        try:
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                post = link.get_attribute('href')
                # print(post)
                if '/p/' in post:
                    posts.append(post)
        except:
            print('Failed Getting Post Links')

        return posts

    def get_user_post_links_soup(self, username):
        # Parse Post Links From User's Page
        posts = []
        if 'instagram.com' in username:
            url = username
        else:
            url = f'https://instagram.com/{username}/?__a=1'
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser").get_text()
        jsondata = json.loads(soup)
        # print(jsondata["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"])
        for post in jsondata["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]:
            post_link = post["node"]["shortcode"]
            # print(post_link)
            posts.append(post_link)
        return posts

    def get_user_link(self, username):
        # Parse Username from Comment Section in Post Page
        username_filter = f'/{username}/'
        users = []
        try:
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                user = link.get_attribute('href')
                if (not '/p/' in user) and (not '/direct/' in user) and (not '/blog/' in user) and (
                        not '/explore/' in user) and (not '/accounts/' in user) and (not '/legal/' in user) and (
                        not 'facebook' in user) and (not '/directory/' in user) and (not '/web/' in user) and (
                        not '/about/' in user) and (not 'help' in user) and (not '//about' in user) and (
                        not username_filter in user):
                    if user != 'https://www.instagram.com/' and user not in users:
                        users.append(user)
            # print(users)
        except:
            print('Failed Getting Post Links')

        return users

    def get_user_link_soup(self, username):
        # Parse Username from Comment Section in Post Page
        users = []
        url = self.driver.current_url
        url_fixed = f'{url}?__a=1'
        self.driver.get(url_fixed)
        # sleep(10)
        soup = BeautifulSoup(self.driver.page_source, "html.parser").get_text()
        jsondata = json.loads(soup)
        for user in jsondata["graphql"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"]:
            username_parsed = user["node"]["owner"]["username"]
            if username_parsed != username and username_parsed not in users:
                users.append(username_parsed)
                # print(username_parsed)

    def get_liked_by_user_soup(self, shortcode):
        query_hash = 'd5d763b1e2acf209d62d22d184488e57'
        users = []
        url = 'https://www.instagram.com/graphql/query/?query_hash=' + query_hash + '&variables={"shortcode":"' + \
              shortcode + '","include_reel":true,"first":50}'

        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser").get_text()
        jsondata = json.loads(soup)

        liked_count = jsondata["data"]["shortcode_media"]["edge_liked_by"]["count"]
        k = liked_count / 50
        page_count = int(proper_round(k))

        # Check if there's more page
        more_page = jsondata["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["has_next_page"]
        if more_page:
            for i in range(0, page_count):
                for user in jsondata["data"]["shortcode_media"]["edge_liked_by"]["edges"]:
                    username_parsed = user["node"]["username"]
                    if username_parsed not in users:
                        users.append(username_parsed)
                        # print(username_parsed)
                end_cursor = jsondata["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]
                # print(end_cursor)
                url = 'https://www.instagram.com/graphql/query/?query_hash=' + query_hash + '&variables={"shortcode":"' + \
                      shortcode + '","include_reel":true,"first":50,"after":"' + end_cursor + '"}'
                self.driver.get(url)
                soup = BeautifulSoup(self.driver.page_source, "html.parser").get_text()
                jsondata = json.loads(soup)

        else:
            for user in jsondata["data"]["shortcode_media"]["edge_liked_by"]["edges"]:
                username_parsed = user["node"]["username"]
                if username_parsed not in users:
                    users.append(username_parsed)
                    # print(username_parsed)

        # print(users)
        return users

    def get_users_links_from_hashtag_page(self, keyword):
        users = []
        key = keyword.replace('#', '')
        url = f'https://www.instagram.com/explore/tags/{key}/?__a=1'

        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser").get_text()
        jsondata = json.loads(soup)

        for sections in jsondata["data"]["top"]["sections"]:
            for media in sections["layout_content"]["medias"]:
                user_link = media["media"]["user"]["username"]
                if user_link not in users:
                    # print(user_link)
                    users.append(user_link)

        for sections in jsondata["data"]["recent"]["sections"]:
            for media in sections["layout_content"]["medias"]:
                user_link = media["media"]["user"]["username"]
                if user_link not in users:
                    # print(user_link)
                    users.append(user_link)

        # print(users)
        return users

    def parse_search_box(self, keyword):
        self.driver.get('https://instagram.com/')
        rnd_sleep = random.randint(0, 3)
        searchbox = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
        searchbox.clear()
        sleep(rnd_sleep)
        type_me(searchbox, keyword)
        sleep(5)

        users = []
        try:
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                user = link.get_attribute('href')
                # print(user)
                if (not '/p/' in user) and (not '/direct/' in user) and (not '/blog/' in user) and (
                        not '/explore/' in user) and (not '/accounts/' in user) and (not '/legal/' in user) and (
                        not 'facebook' in user) and (not '/directory/' in user) and (not '/web/' in user) and (
                        not '/about/' in user) and (not 'help' in user) and (not '//about' in user):
                    if user != 'https://www.instagram.com/' and user not in users:
                        users.append(user)
            # print(users)
        except:
            print('Failed Getting Post Links')

        return users

    def __del__(self):
        pass
