mport time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from csv import DictReader
import cv2
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def resize(image):
    # 4350px wide and 4032px high. 4350*4032 = 17539200

    value_change = "C:/Users/smoot/PycharmProjects/photo/venv/photos/{}".format(image)
    img = cv2.imread(value_change, cv2.IMREAD_UNCHANGED)

    scale_percent = 17539200 / img.size
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    print('Resized Dimensions : ', resized.shape)

    v = "C:/Users/smoot/PycharmProjects/photo/venv/photos/2{}".format(image)

    cv2.imwrite(v,resized)
    cv2.waitKey(1)
    cv2.destroyAllWindows()





def upload():
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium")
    driver = webdriver.Chrome('C:/Users/smoot/PycharmProjects/photo/chromedriver.exe', options=chrome_options)
    with open("C:/Users/smoot/PycharmProjects/photo/venv/photos/list_of_total.csv") as f:
        a1 = [row["filename"] for row in DictReader(f)]

    with open(r"C:\Users\smoot\PycharmProjects\photo\venv\track.txt") as c:
        a2 = [row["filename"] for row in DictReader(c)]

    with open(r"C:\Users\smoot\PycharmProjects\photo\venv\track.txt", 'a+', newline='') as fd:
        fd.write('\n')
        main_list = np.setdiff1d(a1, a2)
        if main_list[0] == 'INITIALIZING':
            main_list[0] = main_list[1]
        print(main_list[0])

        fd.write(main_list[0])

    resize(main_list[0])

    df = pd.read_csv("C:/Users/smoot/PycharmProjects/photo/venv/photos/list_of_total.csv", sep=',', encoding="cp1252")
    ye = df.loc[df['filename'] == main_list[0]]

    print(ye.iloc[0, 3])
    filename = main_list[0]
    print(filename, 'selected')

    value_change = "C:/Users/smoot/PycharmProjects/photo/venv/photos/2{}".format(filename)
    print(value_change)
    driver.get("https://www.redbubble.com/portfolio/images/new?ref=account-nav-dropdown")

    choosefile = driver.find_element_by_id('select-image-single')
    choosefile.send_keys(value_change)
    title = driver.find_element_by_id('work_title_en')
    title.send_keys(ye.iloc[0,3])
    tags = driver.find_element_by_id('work_tag_field_en')
    tags.send_keys(ye.iloc[0,1],', ',ye.iloc[0,2],', ',ye.iloc[0,4],', ',ye.iloc[0,6],', ',ye.iloc[0,8],', ',ye.iloc[0,5])
    time.sleep(15)
    likes = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Disabled')]")))
    like = driver.find_elements_by_xpath("//div[contains(text(),'Disabled')]")
    for x in range(0, len(like)):
        if like[x].is_displayed():
            like[x].click()
    accept = WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.ID, "rightsDeclaration")))
    safe = driver.find_element_by_id('work_safe_for_work_true')
    #accept = driver.find_element_by_id('rightsDeclaration')
    submit = driver.find_element_by_id('submit-work')
    safe.click()
    safe.click()
    time.sleep(5)
    accept.click()
    submit.click()
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "node_modules--redbubble-design-system-react-TextLink-styles__children--1LPg8")))
    driver.quit()

x = 1
#60 images is the upload limit
while x < 60:
    time.sleep(5)
    upload()
    x = x +1
