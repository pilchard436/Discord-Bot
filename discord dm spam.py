from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import random 

username = 'sanlakh'
msg = "spam"
spam_time = -1

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://discordapp.com")
login = driver.find_element_by_xpath('//*[@id="app-mount"]/div/div/div/header[1]/nav/ul[2]/li[4]/a')
login.click()

driver.implicitly_wait(2)

email = driver.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/input')
email.send_keys("pilchard436@gmail.com")
password = driver.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input')
password.send_keys("Vim_justice123")
login = driver.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]')
login.click()

driver.implicitly_wait(5)

user = driver.find_element_by_link_text(username)
user.click()
if spam_time < 0:
    try:
        while True:
            textbox = driver.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/form/div/div/div/div[3]/div[2]/div')
            textbox.send_keys(msg)
            textbox.send_keys(Keys.RETURN)
            time.sleep(5*random.random())
    except KeyboardInterrupt:
        driver.quit()
else:
    try:
        for i in range(0, spam_time):
            textbox = driver.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/form/div/div/div/div[3]/div[2]/div')
            textbox.send_keys(msg)
            textbox.send_keys(Keys.RETURN)
            time.sleep(5*random.random())
        driver.quit()
    except KeyboardInterrupt:
        driver.quit()



