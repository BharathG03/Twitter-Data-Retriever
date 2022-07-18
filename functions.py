from click import option
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# __________________ Setup Webdriver ___________________

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_service = Service("chromedriver.exe")

driver = webdriver.Chrome(
    service=chrome_service, options=chrome_options)

# __________________ Send Queary ___________________

def search(user="", search_term="", until="", since="", count=10):
    driver.get("https://twitter.com/explore")
    driver.maximize_window()

    search = "lang:en "

    if user != "":
        search += f"(from:{user}) "
    if search_term != "":
        search += f'"{search_term}" '
    if until != "":
        search += f"until:{until} "
    if since != "":
        search += f"since:{since} "

    serach_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input")))
    serach_box.send_keys(search)
    serach_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.LINK_TEXT, "Latest"))).click()

    data = list(get_tweets(count))
    return data


# __________________ Read Tweets  ___________________

def get_tweets(count):
    temp = set()
    c = 0

    while len(temp) < count:
        c += 1
        tweets = driver.find_elements(
            "xpath", "//article[@data-testid='tweet']")

        for tweet in tweets[-15:]:
            try:
                temp_text = tweet.find_element(
                    "xpath", "div/div/div/div[2]/div[2]/div[2]/div[2]/div")
                temp_text = temp_text.find_elements("xpath", "span")

                text = ""

                for _ in temp_text:
                    text += _.text

                if text not in temp and text != "":
                    temp.add(text)

                elif text == "":
                    temp_text = tweet.find_element(
                        "xpath", "div/div/div/div[2]/div[2]/div[2]/div[1]/div")
                    temp_text = temp_text.find_elements("xpath", "span")

                    for _ in temp_text:
                        text += _.text

                    if text != "":
                        temp.add(text)
            except:
                pass
        
        pos = driver.execute_script("return window.pageYOffset;")
        page = driver.find_element("xpath", "//input")
        page.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
        new_pos = driver.execute_script("return window.pageYOffset;")

        if new_pos > 0:
            position_count = 0
            while pos == new_pos:
                position_count += 1
                time.sleep(1)
                if position_count == 10:
                    count = len(temp)
                    break

    return temp