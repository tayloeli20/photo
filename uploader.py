import glob
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")
driver = webdriver.Chrome(options=chrome_options)

photos = 'C:/Users/smoot/PycharmProjects/photo/venv/photos/*.jpg'
time.sleep(2)
list_of_files = glob.glob(
    photos)  # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
filename = latest_file[49:]

print(filename, 'selected')

value_change = "C:/Users/smoot/PycharmProjects/photo/venv/photos/{}".format(filename)
print(value_change)
driver.get("https://www.redbubble.com/portfolio/images/new?ref=account-nav-dropdown")

choosefile = driver.find_element_by_id('select-image-single')


class upload:
    choosefile.send_keys(value_change)
