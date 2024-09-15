import os
import pandas as pd
# from __future__ import annotations
import time, random, os, csv, platform
import logging
import selenium
from bs4 import BeautifulSoup
import pyautogui
import undetected_chromedriver as uc
from urllib.request import urlopen
import re
from datetime import datetime, timedelta
from reducehtml import html_remover, html_mini_remover
import openai
from openai_functions import get_job_links,get_easy_apply_xpath
import pandas as pd
import datetime

easy_apply_selector='div.p5  button.jobs-apply-button'

links_to_use=[float(i.replace('links_to_use_later_','').replace('.csv','')) for i in os.listdir() if 'links_to_use_later_' in i]
df=pd.read_csv(f'links_to_use_later_{max(links_to_use)}.csv')
todrop=df['jobs_link'].tolist()
newdrop=[]
for url in todrop:
    try:
        splitted=url.split('/')
        jobid=splitted[splitted.index('view')+1]
        newdrop.append(f'https://www.linkedin.com/jobs/view/{jobid}')
    except:
         pass


user_data_dir=r"C:\Users\TheQwertyPhoenix\AppData\Local\Google\Chrome\User Data"
profile_directory='Profile 1'

done_in=datetime.datetime.now()
def open_browser(user_data_dir,profile_directory,url):
# log = logging.getLogger(__name__)
# driver = webdriver.Chrome(ChromeDriverManager().install())
    options = uc.ChromeOptions()
    options.add_argument('--user-data-dir='+user_data_dir) 
    options.add_argument(r'--profile-directory='+profile_directory) #e.g. Profile 3
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")

    # Disable webdriver flags or you will be easily detectable
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver=uc.Chrome(options=options)
    driver.get(url)
    return driver
# driver = webdriver.Chrome(ChromeDriverManager().install())
def avoid_lock() -> None:
        x, _ = pyautogui.position()
        pyautogui.moveTo(x + 200, pyautogui.position().y, duration=1.0)
        pyautogui.moveTo(x, pyautogui.position().y, duration=0.5)
        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(0.5)
        pyautogui.press('esc')
def load_page(driver, sleep=1):
        scroll_page = 0
        while scroll_page < 4000:
            driver.execute_script("window.scrollTo(0," + str(scroll_page) + " );")
            scroll_page += 200
            time.sleep(sleep)
def fill_data(driver) -> None:
    driver.set_window_size(1, 1)
    driver.set_window_position(2000, 2000)
    driver.maximize_window()
def scroll_down(selected_to_scroll_from,driver):
    scroll_origin = selenium.webdriver.common.actions.wheel_input.ScrollOrigin.from_element(selected_to_scroll_from)    
    for i in range(30):
        selenium.webdriver.common.action_chains.ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, 200)\
            .perform()
        time.sleep(1)
     
if __name__ == '__main__':
    for url in newdrop:
        driver=open_browser(user_data_dir,profile_directory,url)
        # print('lock')
        avoid_lock()
        fill_data(driver)
        

        # button_xpath=get_easy_apply_xpath(simplified_html)
        # print(button_xpath)
        time.sleep(3)
        driver.find_element(selenium.webdriver.common.by.By.CSS_SELECTOR,easy_apply_selector).click()
        time.sleep(3)
        html = driver.page_source
        simplified_html=html_mini_remover(html)
        print(len(html),len(simplified_html))
        # print(len(easy_apply_button)) #.click()
        time.sleep(100000)

