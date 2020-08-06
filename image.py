from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob
import os
import time
import pandas as pd
from csv import writer

totalList = "C:/Users/smoot/PycharmProjects/photo/venv/photos/list_of_total.csv"


# this function returns the updated info from the csv file so it can go back to where it started
def fileinfo():
    csvr = pd.read_csv(totalList, encoding="cp1252")
    last = csvr.iloc[-1, -2]
    step = csvr.iloc[-1, -1]
    return last, step

# makes download directory priority and initializes browser
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_settings.popups": 0,
         "download.default_directory":
             r"C:\Users\smoot\PycharmProjects\photo\venv\photos\\",  # IMPORTANT - ENDING SLASH V IMPORTANT
         "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome('C:/Users/smoot/PycharmProjects/photo/chromedriver.exe', options=options)

browser.get('https://images.nga.gov/en/search/show_advanced_search_page/?form_name=defaultname')
submit = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "submit"))
)
go = submit.find_element_by_xpath('//*[@id="advancedSearchForm"]/div[2]/div[4]/input[1]')

go.click()

openaccess = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "refinedOpenAccessCheck"))
)

openaccess.click()
time.sleep(5)
main_page = browser.window_handles[0]

#pulled from stockoverflow
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


# navigates to download page popup
def openim():
    try:
        y = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "pictureBox_1")))

        x = y.find_element_by_class_name('imageLink')

        x.click()

        time.sleep(5)

        download_page = browser.window_handles[1]

        browser.switch_to.window(download_page)
    except IndexError:
        # in case the download page hasn't opened
        print('problem in funct openim, attempting to open wait and try again after the page has loaded another 5 '
              'seconds')
        time.sleep(5)
        openim()


# navigates to download page at main_page
def findpage():
    last, step = fileinfo()
    p = str(last)
    value_w = "arguments[0].value = '{}';".format(p)

    head = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "GridHeader")))
    select = head.find_element_by_id('PageSelectBox')

    browser.execute_script(value_w, select)
    time.sleep(15)
    browser.execute_script("arguments[0].onblur();", select)
    time.sleep(10)
    openim()


# this initializing def makes a line in the csv file for the findpage function to find the last page
def init():
    last, step = fileinfo()
    filename = 'INITIALIZING'
    artist = 'artist'
    artistinfo = 'artistino'
    title = 'tit'
    dated = 'dated'
    classif = 'classif'
    medium = 'medium'
    dimensions = 'dimensions'
    credit = 'credit'
    page1 = int(last) + 1
    page = str(page1)
    fields = [filename, artist, artistinfo, title, dated, classif, medium,
              dimensions, credit, page, 1]
    append_list_as_row(totalList, fields)


# goes through and download images in popup
def download():
    time.sleep(5)
    last, step = fileinfo()
    num = int(step)
    empty = []
    append_list_as_row(totalList, empty)
    while num < 26:
        i = str(num)
        try:
            value_change = "arguments[0].value = '{}';".format(i)
            bar = browser.find_element_by_id('PageSelectBox')

            browser.execute_script(value_change, bar)

            browser.execute_script("arguments[0].onchange();", bar)

            z = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "iconDownloadComp"))
            )
            z.click()
        except TimeoutException:
            print('couldnt find da link to download so we skipped')
            browser.close()
            browser.switch_to.window(main_page)
            openim()
            print('couldnt find da link to download so we skipped')
            num = num + 1
            v = str(num)
            value_change = "arguments[0].value = '{}';".format(v)
            bar = browser.find_element_by_id('PageSelectBox')
            browser.execute_script(value_change, bar)
            browser.execute_script("arguments[0].onchange();", bar)

        photos = 'C:/Users/smoot/PycharmProjects/photo/venv/photos/*.jpg' # * means all if need specific format then *.csv

        time.sleep(2)
        list_of_files = glob.glob(
            photos)

        # list_of_files.remove(max(list_of_files, key=os.path.getctime))

        latest_file = max(list_of_files, key=os.path.getctime)
        filename = latest_file[49:]
        print(filename)
        try:
            # NOTE if you change the the popup browsers size then it changes XPATH of the element
            artist = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div[3]/dl/dd[1]').text
            artistinfo = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div[3]/dl/dd[2]').text
            title = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div[3]/dl/dd[3]').text
            dated = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div[3]/dl/dd[4]').text
            classif = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div[3]/dl/dd[5]').text
            medium = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div[3]/dl/dd[6]').text
            dimensions = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div[3]/dl/dd[7]').text
            credit = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div[3]/dl/dd[8]').text
            page = str(last)
            slide = str(num)
        except NoSuchElementException:
            print('image info is over a div')
            artist = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[3]/dl/dd[1]').text
            artistinfo = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[3]/dl/dd[2]').text
            title = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[3]/dl/dd[3]').text
            dated = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[3]/dl/dd[4]').text
            classif = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[3]/dl/dd[5]').text
            medium = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[3]/dl/dd[6]').text
            dimensions = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[3]/dl/dd[7]').text
            credit = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div[3]/dl/dd[8]').text
            page = str(last)
            slide = str(num)

        fields = [filename, artist, artistinfo, title, dated, classif, medium,
                  dimensions, credit, page, slide]

        append_list_as_row(totalList, fields)

        num = num + 1
    init()
    browser.close()


class Setup:
    last, step = fileinfo()

    findpage()
    # *you need to have an exception to this  error*
    #  raise TimeoutException(message, screen, stacktrace)       ----COMPLETED---
    #  selenium.common.exceptions.TimeoutException: Message:
    download()

    browser.switch_to.window(main_page)

    p = str(last)

    value_c = "arguments[0].value = '{}';".format(p)

    head = browser.find_element_by_id('GridHeader')
    select = head.find_element_by_id('PageSelectBox')

    browser.execute_script(value_c, select)
    browser.execute_script("arguments[0].onblur();", select)
    browser.quit()
