#! python3
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import bs4, requests, smtplib
import dateutil.parser as dparser
import fbchat
import base64
import time

# Gather data from webpage
get_page = requests.get('https://www.ozbargain.com.au/cat/mobile')
get_page.raise_for_status() # Check if request was successful

# Parse html data and filter
data = bs4.BeautifulSoup(get_page.text, 'html.parser')
deals = data.select('.node-ozbdeal')

for d in deals:
    try:

        # if Boost deal found, send facebook notification
        if "BOOST" in d.h2['data-title'].upper():
            date_str = d.find("div", {"class": "submitted"})
            date_str = date_str.find('strong').next_sibling
            date = dparser.parse(date_str,fuzzy=True,dayfirst=True)

            # Check if deal is from today
            if date.date() == (datetime.today().date()):
                link = "https://www.ozbargain.com.au" + d.h2.a['href']
                try:
                    browser = webdriver.Chrome()
                    browser.get('http://messenger.com')
                    delay = 3  # seconds

                    username = WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.ID, 'email')))  # Wait to click the login form to input details
                    username.send_keys('username')
                    password = WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.ID, 'pass')))
                    password.send_keys('password')
                    password.submit()

                    chat = browser.find_element_by_xpath("//div[@data-tooltip-content='ok guccio gucci']")
                    chat.click()

                    text_box = browser.find_element_by_xpath("//div[@aria-label='Type a message...']")
                    text_box.click()

                    text_box.send_keys(link)
                    send_btn = browser.find_element_by_xpath("//a[@aria-label='Send']")
                    time.sleep(1)
                    send_btn.click()

                finally:
                    browser.quit()
                                
    except KeyError:
        continue


