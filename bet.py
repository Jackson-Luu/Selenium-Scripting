#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome()
browser.get('http://messenger.com')
delay = 3  # seconds

username = WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.ID, 'email')))  # Wait to click the login form to input details
username.send_keys('username')
password = WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.ID, 'pass')))
password.send_keys('password')
password.submit()

# Click on tips chat

chat = browser.find_element_by_xpath("//div[@data-tooltip-content='FNBATSubs']")
chat.click()

# Find recent messages

wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//time')))
timestamps = browser.find_elements_by_xpath('//time')

days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
bets = []

for t in timestamps:

    # Ignore messages not from today

    is_today = True
    for d in days:
        if d in t.text:
            is_today = False
            break

    if is_today:
        messages = browser.find_elements_by_xpath("//div[@data-tooltip-content='" + t.text + "']")
        for m in messages:
            msg = m.find_element_by_xpath('./div').get_attribute('aria-label')

            if '🔥' in msg:
                continue
            elif 'Multi' not in msg:
                continue
            else:
                bet = []
                lines = msg.splitlines()
                parse = False
                for l in lines:
                    if 'Multi' in l:
                        parse = True
                        continue
                    if not l and parse:
                        parse = False
                        bets.append(bet)
                        bet = []
                        continue
                    if parse:
                        bet.append(l)