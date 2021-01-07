import faster_than_requests as r
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import logging
import sys

source = r.get2str("https://pastebin.com/raw/jr5qpQEm")

driver = webdriver.Firefox()
driver.get('https://discord.com/login')

email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]')))

email.send_keys('YOUR_DISCORD_EMAIL')
password.send_keys('YOUR_DISCORD_PASSWORD')
submit.click()
time.sleep(15) # time to enter 2FA code
driver.get('https://discord.com/channels/@me/ID_OF_YOUR_DISCORD_CHAT_WITH_POKEMON_BOT')
try:
    textbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//form//div[@role="textbox"]')))
except:
    driver.close()
    logging.error('Unable to find Discord message textbox. Likely due to failed login.')
    sys.exit()

commands = source.split('\n')
for command in commands:
    textbox.send_keys(command[::-1])
    textbox.send_keys(Keys.ENTER)
    time.sleep(3) # wait 3s for Discord bot to process command
driver.close()
