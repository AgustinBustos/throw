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
from openai_functions import get_job_links,get_easy_apply_xpath,get_answers
import pandas as pd
import datetime
from selenium.webdriver.support.ui import Select



easy_apply_selector='div.p5  button.jobs-apply-button'
next_button_selector="button[aria-label='Continue to next step']"
review_button_selector="button[aria-label='Review your application']"
error_in_task='''div[role='alert'] li-icon[aria-hidden="true"]'''
all_of_form_parts='div.jobs-easy-apply-form-section__grouping'
submiter='''button[aria-label='Submit application']'''


links_to_use=[float(i.replace('links_to_use_later_','').replace('.csv','')) for i in os.listdir() if 'links_to_use_later_' in i]
df=pd.read_csv(f'links_to_use_later_{max(links_to_use)}.csv')
# todrop=df['jobs_link'].tolist()

def get_id(url):
    try:
        splitted=url.split('/')
        jobid=splitted[splitted.index('view')+1]
        return f'https://www.linkedin.com/jobs/view/{jobid}'
    except:
        return 'NaN'
df['job_id']=df['jobs_link'].apply(get_id)
df['sent']='No'
df.to_csv(f'links_to_use_later_{max(links_to_use)}.csv',index=False)
newdrop=[i for i in df['job_id'].tolist() if i!='NaN']

user_data_dir=r"C:\Users\TheQwertyPhoenix\AppData\Local\Google\Chrome\User Data"
profile_directory='Profile 1'

css_selector=selenium.webdriver.common.by.By.CSS_SELECTOR
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
def responder(form_parts_with_errors,index,i):
    time.sleep(2)
    select_element=form_parts_with_errors[index].find_elements(css_selector,'select')
    input_elements=form_parts_with_errors[index].find_elements(css_selector,'input')
    textarea=form_parts_with_errors[index].find_elements(css_selector,'textarea')
    if textarea:
        textarea[0].send_keys(i)
    elif select_element:
        select = Select(select_element[0])
        select.select_by_visible_text(i)
    elif len(input_elements)==1:   
        input_elements[0].send_keys(i)
    else:
        labeling=form_parts_with_errors[index].find_elements(css_selector,'label')
        labeling[0].click()
        for j in range(len(labeling)):
            time.sleep(1)
            labeling=form_parts_with_errors[index].find_elements(css_selector,'label')
            if labeling[j].text==i:
                labeling[j].click()    
if __name__ == '__main__':
    driver=open_browser(user_data_dir,profile_directory,'https://www.google.com/')
    time.sleep(10)
    
    for url in newdrop:
        time.sleep(random.choice([i for i in range(10)]))
        try:
            driver.get(url)
            
            # print('lock')
            avoid_lock()
            fill_data(driver)
            

            # button_xpath=get_easy_apply_xpath(simplified_html)
            # print(button_xpath)
            time.sleep(3)
            driver.find_element(css_selector,easy_apply_selector).click()
            time.sleep(3)
            form_intents=0
            for i in range(10):
                next_page=driver.find_elements(css_selector,next_button_selector)
                review=driver.find_elements(css_selector,review_button_selector)
                form_parts=driver.find_elements(css_selector,all_of_form_parts)
                form_parts_with_errors=[i for i in form_parts if i.find_elements(css_selector,error_in_task)]
                submit=driver.find_elements(css_selector,submiter)
                if form_parts_with_errors:
                    form_intents+=1
                    if form_intents>=2:
                        break
                    #just do send keys and select
                    answers=get_answers(str([i.get_attribute('outerHTML') for i in form_parts_with_errors]))
                    # print(answers)
                    for index,i in enumerate(answers):
                        #have to interact better
                        responder(form_parts_with_errors,index,i)
                        

                    time.sleep(2)
                    if next_page:
                        next_page[0].click()
                    else:
                        review[0].click()     
                    # time.sleep(10000)
                elif next_page:
                    form_intents=0
                    next_page[0].click()
                elif review:
                    form_intents=0
                    review[0].click()
                elif submit:
                    form_intents=0
                    submit[0].click()
                    df.loc[df['job_id']==url,'sent']='Yes'
                    df.to_csv(f'links_to_use_later_{max(links_to_use)}.csv',index=False)
                    # time.sleep(10000)

                time.sleep(3)
                # time.sleep(100000)

            # html = driver.page_source
            # simplified_html=html_mini_remover(html)
            # # print(len(html),len(simplified_html))
            # # print(len(easy_apply_button)) #.click()

            # time.sleep(100000)
        except Exception as e:
            print(e)
            # time.sleep(100000)
        time.sleep(10000)
    driver.quit()
