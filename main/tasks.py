import json
import logging
import os
import time
import urllib
import faktory
from bs4 import BeautifulSoup, Tag
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.MongoConnection import MongoConnnection
from utils.utils import URL_FACTORY, URL_FACEBOOK_ROOT, is_valid_email, is_url, URL_FACEBOOK_LIVE_SEE_ALL, \
    MOZILLA_DRIVER_PATH
from selenium import webdriver
import re

logging.basicConfig(level=logging.INFO)


def get_browser():

    options = Options()
    options.headless = True

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.cache.disk.enable", False)
    fp.set_preference("browser.cache.memory.enable", False)
    fp.set_preference("browser.cache.offline.enable", False)
    fp.set_preference("network.http.use-cache", False)
    fp.update_preferences()
    browser = webdriver.Firefox(executable_path=MOZILLA_DRIVER_PATH, options=options, firefox_profile=fp)
    browser.implicitly_wait(30)
    browser.maximize_window()
    browser.delete_all_cookies()
    return browser


def live_see_all():
    try:
        browser = get_browser()
        browser.get(URL_FACEBOOK_LIVE_SEE_ALL)
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    except Exception as e:
        browser.quit()
        logging.log(logging.CRITICAL, e)
        raise e

    try:
        soup = BeautifulSoup(browser.page_source, 'lxml')
        link_tags = soup.find_all("a")
        uid_list = []
        for tag in link_tags:
            if all(each in tag.attrs for each in ['uid', 'data-hovercard']):
                uid = tag['uid']
                if uid not in uid_list:
                    uid_list.append(uid)
        browser.quit()
    except Exception as e:
        logging.log(logging.CRITICAL, "Dom changed in live_see_all page, report admin!")
        browser.quit()
        return
    print(json.dumps(uid_list))
    with faktory.connection(faktory=URL_FACTORY) as client:
        for uid in uid_list[:5]:
            client.queue('parse_profile', args=[uid], queue='busy')


def parse_profile(uid):

    try:
        url = urllib.parse.urljoin(URL_FACEBOOK_ROOT, uid)
        browser = get_browser()
        wait = WebDriverWait(browser, 10)
        wait.until(EC.url_changes(url))
        browser.get(url)
    except Exception as e:
        browser.quit()
        logging.log(logging.CRITICAL, e)
        raise e

    soup = BeautifulSoup(browser.page_source, 'lxml')
    user_data = dict()
    user_data['uid'] = uid
    user_data['profile_url'] = browser.current_url

    # get username
    user_data['username'] = browser.current_url.replace(URL_FACEBOOK_ROOT, '').replace('/', '')

    # Get user's name
    user_name_h1 = soup.select('h1#seo_h1_tag')
    if user_name_h1 and len(user_name_h1) == 1 and user_name_h1[0].span:
        user_data['name'] = user_name_h1[0].span.string
    else:
        logging.log(logging.CRITICAL, f'Dom changed for name parse, report admin! Profile : {browser.current_url}')
        browser.quit()
        return

    # Get follower number
    follower_count = soup.find('div', string=re.compile('people follow this'))
    if follower_count:
        user_data['followers'] = follower_count.string.split(' ')[0].replace(',', '')
    else:
        logging.log(logging.CRITICAL, f'Dom changed for follower count parse, report admin! Profile : {browser.current_url}')
        browser.quit()
        return

    # Get likes number
    likes_count = soup.find('div', string=re.compile('people like this'))
    if likes_count:
        user_data['likes'] = likes_count.string.split(' ')[0].replace(',', '')
    else:
        logging.log(logging.CRITICAL, f'Dom changed for likes count parse, report admin! Profile : {browser.current_url}')
        browser.quit()
        return

    try:
        about_page = browser.find_element(By.CSS_SELECTOR, "[data-key=tab_about]")
        about_page.click()
        time.sleep(10)
    except Exception as e:
        logging.log(logging.CRITICAL, e)
        browser.quit()
        return

    soup = BeautifulSoup(browser.page_source, 'lxml')

    # CONTACT DETAILS
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

    else:
        logging.log(logging.CRITICAL, f'Dom changed for CONTACT DETAILS, report admin! Profile : {browser.current_url}')
        browser.quit()
        return

    browser.quit()

    mongo_conn = MongoConnnection.Instance()
    mongo_conn.get_collection("user_details").find_one_and_replace({'uid': user_data['uid']}, user_data, upsert=True)

    with faktory.connection(faktory=URL_FACTORY) as client:
        if user_data.get('username', None):
            client.queue('parse_posts', args=[user_data['uid'], user_data['username']], queue='busy')


def parse_posts(uid, username):

    try:
        url = '/'.join([URL_FACEBOOK_ROOT, 'pg', username, 'posts/'])
        browser = get_browser()
        browser.get(url)
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except Exception as e:
        browser.quit()
        logging.log(logging.CRITICAL, e)
        raise e

    soup = BeautifulSoup(browser.page_source, 'lxml')
    k = soup.find_all(class_="_5pcr userContentWrapper")
    mongo_conn = MongoConnnection.Instance()

    for item in k:
        # Post Text
        actual_posts = item.find_all(attrs={"data-testid": "post_message"})
        post_dict = dict()
        post_dict['uid'] = uid

        dt = item.find("abbr")
        if dt:
            post_dict['utc_timestamp'] = dt['data-utime']
            post_ids = [each for each in re.findall("/(\\d+)?", dt.parent['href']) if each]
            post_dict['post_id'] = post_ids[0]
        else:
            logging.log(logging.CRITICAL, 'Dom changed for post date time, report admin')
            continue

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

        mongo_conn.get_collection("posts").find_one_and_replace({'uid': uid, 'post_id': post_dict['post_id']},
                                                                post_dict, upsert=True)
    browser.quit()



