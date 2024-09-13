import os
import pandas as pd
from __future__ import annotations
import time, random, os, csv, platform
import logging
import selenium
from bs4 import BeautifulSoup
import pyautogui
import undetected_chromedriver as uc
from urllib.request import urlopen
import re
from datetime import datetime, timedelta
from reducehtml import html_remover
import openai
from openai_functions import get_job_links
import pandas as pd
import datetime


links_to_use=[float(i.replace('links_to_use_later_','').replace('.csv','')) for i in os.listdir() if 'links_to_use_later_' in i]
df=pd.read_csv(f'links_to_use_later_{max(links_to_use)}.csv')
todrop=df['jobs_link'].tolist()
print(todrop)
