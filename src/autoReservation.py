import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

import time
import pyautogui
import pyperclip

TIMEOUT_SECONDS = 5
NAVER_ID = os.getenv('NAVER_ID')
NAVER_PASSWORD = os.getenv('NAVER_PASSWORD')
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

def login(url):
    driver.get(url)
    element = WebDriverWait(driver, TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#log\.login')))

    id = driver.find_element(By.CSS_SELECTOR, '#id')
    id.click()
    pyperclip.copy(NAVER_ID)
    pyautogui.keyDown('command')
    pyautogui.press('v')
    pyautogui.keyUp('command')

    pw = driver.find_element(By.CSS_SELECTOR, '#pw')
    time.sleep(1)
    pw.click()
    pyperclip.copy(NAVER_PASSWORD)
    pyautogui.keyDown('command')
    pyautogui.press('v')
    pyautogui.keyUp('command')

    loginBtn = driver.find_element(By.CSS_SELECTOR, '#log\.login')
    time.sleep(1)
    loginBtn.click()

def autoReservation(retry, url):
    if retry > 5:
        return

    element = WebDriverWait(driver, TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#calendar > div > strong')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    month = soup.select_one('#calendar > div > strong > span:nth-child(2)')
    if '1' in month.text:
        nextMonthBtn = driver.find_element(By.CSS_SELECTOR, '#calendar > div > a.calendar-btn.calendar-btn-next-mon')
        nextMonthBtn.click()
        time.sleep(0.1)

    element = WebDriverWait(driver, TIMEOUT_SECONDS).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#calendar > table > tbody:nth-child(3) > tr:nth-child(4) > td.calendar-sun > a')))
    day = driver.find_element(By.CSS_SELECTOR, '#calendar > table > tbody:nth-child(3) > tr:nth-child(4) > td.calendar-sun > a')
    day.click()
    time.sleep(0.2)

    try:
        timeBtn = driver.find_element(By.CSS_SELECTOR, '#container > bk-restaurant > div > div > div.wrap_right > div.section_booking > div > bk-select-condition > bk-select-time > div > div > div > ul > li:nth-child(1) > a > span')
        timeBtn.click()
        time.sleep(0.2)
    except:
        driver.get(url)
        time.sleep(0.05)
        autoReservation(retry + 1, url)

    plusBtn = driver.find_element(By.CSS_SELECTOR, '#container > bk-restaurant > div > div > div.wrap_right > div.section_booking > div > div > bk-restaurant-qty-selector > div > div:nth-child(2) > div.price_control > div.count_control > a.btn_plus_minus.spr_book.ico_plus3')
    plusBtn.click()
    plusBtn.click()

    orderBtn = driver.find_element(By.CSS_SELECTOR, '#container > bk-restaurant > div > div > div.wrap_right > bk-submit > div > button')
    time.sleep(0.2)
    orderBtn.click()

    print('hello')

if __name__ == '__main__':
    url = 'https://booking.naver.com/booking/6/bizes/57148/items/4692569'
    login(url)
    driver.get(url)
    while True:
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            break
    driver.get(url)
    autoReservation(0, url)