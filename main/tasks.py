import json
import logging
import os
import re
import time
import urllib
import faktory
from bs4 import BeautifulSoup, Tag
from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from utils import URL_FACTORY, URL_FACEBOOK_ROOT, is_valid_email, is_url, URL_FACEBOOK_LIVE_SEE_ALL, MONGODB_URI
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)


def get_driver():

    options = Options()
    options.headless = True

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.cache.disk.enable", False)
    fp.set_preference("browser.cache.memory.enable", False)
    fp.set_preference("browser.cache.offline.enable", False)
    fp.set_preference("network.http.use-cache", False)
    fp.update_preferences()

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options, firefox_profile=fp)
    driver.maximize_window()
    driver.delete_all_cookies()
    return driver


def check_height(driver, old_height):
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


def live_see_all(num_user_to_parse, num_post_scroll):
    try:
        driver = get_driver()
        driver.get(URL_FACEBOOK_LIVE_SEE_ALL)

        scroll_time = 8
        total_scrolls = 150
        current_scrolls = 0
        while True:
            try:
                if current_scrolls == total_scrolls:
                    break
                old_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, scroll_time, 1).until(lambda driver: check_height(driver, old_height))
                current_scrolls += 1
            except TimeoutException:
                break

        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.quit()
    except Exception as e:
        driver.quit()
        raise e

    try:
        link_tags = soup.find_all("a")
        uid_list = []
        for tag in link_tags:
            if all(each in tag.attrs for each in ['uid', 'data-hovercard']):
                uid = tag['uid']
                if uid not in uid_list:
                    uid_list.append(uid)
    except Exception as e:
        raise e

    logging.log(logging.INFO, f"Total live users : {len(uid_list)}")
    with faktory.connection(faktory=URL_FACTORY) as client:
        if type(num_user_to_parse) == int and num_user_to_parse < len(uid_list):
            uid_list = uid_list[:num_user_to_parse]
        for uid in uid_list:
            client.queue('parse_profile', args=[uid, num_post_scroll], queue='busy')


def parse_profile(uid, num_post_scroll):

    try:
        url = urllib.parse.urljoin(URL_FACEBOOK_ROOT, uid)
        driver = get_driver()
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        current_url = driver.current_url
    except Exception as e:
        driver.quit()
        raise e

    try:
        user_data = dict()
        user_data['uid'] = uid
        user_data['profile_url'] = current_url

        # get username
        user_data['username'] = current_url.replace(URL_FACEBOOK_ROOT, '').replace('/', '')

        # Get user's name
        # user_name_h1 = soup.find("h1", id="seo_h1_tag")
        user_name_div = soup.find("div", id="u_0_0")
        user_data['name'] = user_name_div.a.span.string

        # Get follower number
        follower_count = soup.find('div', string=re.compile('people follow this'))
        if follower_count:
            res = re.findall('[0-9,]+', follower_count.string)
            if res:
                user_data['followers'] = res[0].replace(',', '')
            else:
                user_data['followers'] = '0'

        # Get likes number
        likes_count = soup.find('div', string=re.compile('people like this'))
        if likes_count:
            res = re.findall('[0-9,]+', likes_count.string)
            if res:
                user_data['likes'] = res[0].replace(',', '')
            else:
                user_data['likes'] = '0'

        # Click about tab for contact details.
        about_page = driver.find_element(By.CSS_SELECTOR, "[data-key=tab_about]")
        about_page.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "PagesProfileAboutInfoPagelet_"+str(uid))))

        # CONTACT DETAILS
        soup = BeautifulSoup(driver.page_source, 'lxml')
        contact_details = []
        cd_div_child = soup.find("div", string='CONTACT DETAILS')
        if cd_div_child:
            for sibling in cd_div_child.next_siblings:
                if type(sibling) is Tag:
                    text_div = sibling.find("div", class_="_50f4")
                    if text_div:
                        if is_valid_email(text_div.string) or is_url(text_div.string):
                            contact_details.append(text_div.string)
                        elif text_div.string.startswith('Call '):
                            contact_details.append(text_div.string.replace('Call', '').strip())
                        elif text_div.parent.name == "a":
                            contact_details.append(text_div.parent['href'])

            user_data['contact_details'] = contact_details
        driver.quit()
    except Exception as e:
        driver.quit()
        logging.log(logging.CRITICAL, f"Parse profile failed : {user_data['profile_url']}")
        raise e

    m_connection = MongoClient(MONGODB_URI)
    with m_connection:
        m_connection.aggero_fb.user_details.find_one_and_replace({'uid': user_data['uid']}, user_data, upsert=True)

    logging.log(logging.INFO, f"User Data : {user_data}")
    with faktory.connection(faktory=URL_FACTORY) as client:
        client.queue('parse_posts', args=[user_data['uid'], user_data['username'], num_post_scroll], queue='busy')


def parse_posts(uid, username, num_post_scroll):

    try:
        url = '/'.join([URL_FACEBOOK_ROOT, 'pg', username, 'posts/'])
        driver = get_driver()
        driver.get(url)

        scroll_time = 8
        total_scrolls = num_post_scroll
        current_scrolls = 0

        while True:
            try:
                if current_scrolls == total_scrolls:
                    break
                old_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, scroll_time, 1).until(lambda driver: check_height(driver, old_height))
                current_scrolls += 1
            except TimeoutException:
                break
    except Exception as e:
        driver.quit()
        raise e

    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        k = soup.find_all(class_="_5pcr userContentWrapper")
        driver.quit()
    except Exception as e:
        driver.quit()
        raise e

    m_connection = MongoClient(MONGODB_URI)
    with m_connection:
        for item in k:
            try:
                # Post Text
                actual_posts = item.find_all(attrs={"data-testid": "post_message"})
                post_dict = dict()
                post_dict['uid'] = uid

                dt = item.find("abbr")
                post_dict['utc_timestamp'] = dt['data-utime']
                post_ids = [each for each in re.findall("/(\\d+)?", dt.parent['href']) if each]
                post_dict['post_id'] = post_ids[0]

                for posts in actual_posts:
                    paragraphs = posts.find_all('p')
                    text = ""
                    for index in range(0, len(paragraphs)):
                        text += paragraphs[index].text

                    post_dict['Post'] = text
                    post_dict['hashtag'] = re.findall("#\\w+", text)

                # Links
                post_links = item.find_all(class_="_6ks")
                p_links = []
                for postLink in post_links:
                    if postLink.a:
                        p_links.append(postLink.find('a').get('href'))
                post_dict['Link'] = p_links

                # Images
                post_pictures = item.find_all(class_="scaledImageFitWidth img")
                post_images = []
                for postPicture in post_pictures:
                    post_images.append(postPicture.get('src'))
                post_dict['Image'] = post_images

                m_connection.aggero_fb.posts.find_one_and_replace({'uid': uid, 'post_id': post_dict['post_id']},
                                                                        post_dict, upsert=True)
            except Exception as e:
                logging.log(logging.CRITICAL, e)
                continue

    logging.log(logging.INFO, f"Parse posts done for user: {os.path.join(URL_FACEBOOK_ROOT, username)}")
    driver.quit()



