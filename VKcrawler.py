import getpass
import calendar
import os
import platform
import sys

import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# -------------------------------------------------------------
# -------------------------------------------------------------


# Global Variables

driver = None

# whether to download photos or not
download_uploaded_photos = True
download_friends_photos = True

# whether to download the full image or its thumbnail (small size)
# if small size is True then it will be very quick else if its false then it will open each photo to download it
# and it will take much more time
friends_small_size = True
photos_small_size = True

total_scrolls = 5000
current_scrolls = 0
scroll_time = 5

old_height = 0

def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height

def data_collector(data, tag):
    if tag == "about_part":
        f = open("About.txt", "w", encoding = "utf-8", newline='\n')
        f.write(str(data))
    if tag == "group_part":
        f = open("Group.txt", "w", encoding = "utf-8", newline='\n')
        f.write(str(data))
    if tag == "friends_part":
        f = open("Friends.txt", "w", encoding = "utf-8", newline='\n')
        f.write(str(data))
    else:
        print("Bad")

def scroll():
    global old_height
    current_scrolls = 0

    while (True):
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 0.05).until(lambda driver: check_height())
            current_scrolls += 1
        except TimeoutException:
            break

    return


def group(id):
    print('Groups:')
    print('--------------------------')
    tag = "group_part"
    try:
        driver.find_element_by_xpath('//div[@class="label fl_l"]/a').click()
        time.sleep(5)
        scroll()
        group = driver.find_elements_by_xpath('//div[@class="group_row_labeled"]/a')
        num_page_items = len(group)
        data = []
        for i in range(num_page_items):
            links = group[i].text + " : " + group[i].get_attribute('href')
            data.append(links)
        time.sleep(5)
        data_collector(data, tag)
        driver.find_element_by_xpath('//div[@class="ui_ownblock_label"]').click()
    except:
        print("Some issue")
    print('======Groups done======')


def friends(id):
    print('Friends:')
    print('--------------------------')
    tag = "friends_part"
    try:
        driver.find_element_by_xpath('//div[@id="profile_friends"]/a[2]').click()
        time.sleep(5)
        scroll()
        time.sleep(5)
        aTagsInLi = driver.find_elements_by_xpath('//div[@class="friends_field friends_field_title"]/a')
        num_page_items = len(aTagsInLi)
        data = []
        for i in range(num_page_items):
            links = aTagsInLi[i].text + " : " + aTagsInLi[i].get_attribute('href')
            data.append(links)
        data_collector(data, tag)
    except:
        print("Some issue")          
    print('======Friends done======')

def about(id):
    print('About:')
    print('--------------------------')
    tag = "about_part"
    try:
        driver.find_element_by_xpath('//a[@class="profile_more_info_link"]').click()
        about = driver.find_elements_by_xpath('//div[@class="clear_fix profile_info_row "]')
        num_page_items = len(about)
        data = []
        for i in range(num_page_items):
            links = about[i].text
            data.append(links)
        data_collector(data, tag)
    except:
        print("Some issue")      
    print('======About done======')


def scrap_profile(ids):
    folder = os.path.join(os.getcwd(), "Data")

    if not os.path.exists(folder):
        os.mkdir(folder)

    os.chdir(folder)

    # execute for all profiles given in input.txt file
    for id in ids:
        
        time.sleep(2)
        driver.get(id)
        time.sleep(2)
        about(id)
        time.sleep(2)
        group(id)
        time.sleep(2)
        friends(id)
        
        print("\nScraping:", id)

        try:
            if not os.path.exists(os.path.join(folder, id.split('/')[-1])):
                os.mkdir(os.path.join(folder, id.split('/')[-1]))
            else:
                print("A folder with the same profile name already exists."
                      " Kindly remove that folder first and then run this code.")
                continue
            os.chdir(os.path.join(folder, id.split('/')[-1]))
        except:
            print("Some error occurred in creating the profile directory.")
            continue

    print("----------------------------------------")
    driver.close()
def login(email, password):
    """ Logging into our own profile """

    try:
        global driver

        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")

        try:
            platform_ = platform.system().lower()
            if platform_ in ['linux', 'darwin']:
                driver = webdriver.Chrome(
                    executable_path="/home/home/PycharmProjects/untitled/Ultimate-Facebook-Scraper-master/Code/chromedriver",
                    options=options)
            else:
                driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
        except:
            print("Kindly replace the Chrome Web Driver with the latest one from: "
                  "http://chromedriver.chromium.org/downloads"
                  "\nYour OS: {}".format(platform_)
                  )
            exit()

        driver.get("https://vk.com/")
        driver.maximize_window()
        time.sleep(2)

        # filling the form
        driver.find_element_by_xpath('//*[@id="index_email"]').send_keys(email)
        driver.find_element_by_xpath('//*[@id="index_pass"]').send_keys(password)
        driver.find_element_by_id('index_login_button').click()



    except Exception as e:
        print("There's some error in log in.")
        print(sys.exc_info()[0])
        exit()









def main():
    ids = ["https://vk.com/" + line.split("/")[-1] for line in open("input.txt")]

    if len(ids) > 0:
        # Getting email and password from user to login into his/her profile
        email = '+380501769110'
        password = 'Normal4568'
        print("\nStarting Scraping...")

        login(email, password)
        scrap_profile(ids)
        # driver.close()
    else:
        print("Input file is empty..")


# -------------------------------------------------------------
# -------------------------------------------------------------

if __name__ == '__main__':
    # get things rolling
    main()







