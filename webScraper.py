from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import time

s = time.time()
# __________________ Setup ___________________

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_service = Service("chromedriver.exe")

user = input("Specific User: ") 
search_term = input("Search Terms: ")
until = input("Until: ")
since = input("Since: ")
count = int(input("Num Entries: "))

driver = webdriver.Chrome(
    service=chrome_service, options=chrome_options)


# __________________ Send Queary ___________________

def search():
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
    
    serach_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input")))
    serach_box.send_keys(search)
    serach_box.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[2]/nav/div/div[2]/div/div[2]"))).click()


# __________________ Read Tweets  ___________________

def get_tweets():
    temp = set()

    while len(temp) < count:
        tweets = driver.find_elements(
            "xpath", "//article[@data-testid='tweet']")
        
        c = 0
        d = 0
        e = 0
        for tweet in tweets:
            try:
                time = tweet.find_element("xpath" "//time").get_attribute("datetime")
                temp_text = tweet.find_element(
                    "xpath", "div/div/div/div[2]/div[2]/div[2]/div[2]/div")
                temp_text = temp_text.find_elements("xpath", "span")

                text = ""


                for _ in temp_text:
                    text += _.text
                
                if text not in temp and text != "":
                    temp.add(text)
                    #print(text)
                    #print("________________________________________________")

                elif text == "":
                    temp_text = tweet.find_element(
                        "xpath", "div/div/div/div[2]/div[2]/div[2]/div[1]/div")
                    temp_text = temp_text.find_elements("xpath", "span")

                    for _ in temp_text:
                        text += _.text

                    if text != "":
                        temp.add(text)
                        #print(text)
                        #print("________________________________________________")
            except:
                pass
            
        #print((c, d, e, len(tweets), len(temp)))
        pos = driver.execute_script("return window.pageYOffset;")
        page = driver.find_element("xpath", "//input")
        page.send_keys(Keys.PAGE_DOWN)
        #driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")
        time.sleep(0.1)
        new_pos = driver.execute_script("return window.pageYOffset;")
    
    return temp



search()
time.sleep(1)
l = get_tweets()
time.sleep(4)

print(len(l))

e = time.time()

print(e - s)

driver.quit()