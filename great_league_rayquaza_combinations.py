from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import re

pokemon_name = "Rayquaza"

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get("https://pokemon.gameinfo.io/en/tools/cp-calculator")

pokemon = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "vs__search")))
level, attack, defense, stamina = driver.find_elements_by_xpath("//input[@type='number']")

pokemon.send_keys(pokemon_name)
pokemon.send_keys(Keys.RETURN)
level.clear()
level.send_keys("15") # level 15 because it's from a research

start_index = 1 # 0 for no friendship, 1 for Good Friends, 2 for Great Friends, 3 for Ultra Friends, 5 for Best Friends
combinations = []
for a in range(start_index, 16):
    attack.clear()
    attack.send_keys(str(a))
    for d in range(start_index, 16):
        defense.clear()
        defense.send_keys(str(d))
        for s in range(start_index, 16):
            stamina.clear()
            stamina.send_keys(str(s))
            cp = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cp']/span"))).text)
            if cp <= 1500:
                combinations.append((a, d, s))

driver.get("https://pogostat.com")

pokelist = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "poke")))
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@id='cp_cap']/following-sibling::button")))
min_iv = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "min_iv"))))
attack = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "att_iv"))))
defense = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "def_iv"))))
stamina = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sta_iv"))))
product = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "stat_prod")))

pokelist.send_keys(pokemon_name)
min_iv.select_by_value(str(start_index))
product.click()

best_combination = (-1, -1, -1)
max_stat_product = -1

for combination in combinations:
    attack.select_by_value(str(combination[0]))
    defense.select_by_value(str(combination[1]))
    stamina.select_by_value(str(combination[2]))
    button.click()

    data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[2]/div[7]"))).text
    stat_product = int(re.sub("^[^%]+% \(", "", data)[:-1])
    if stat_product > max_stat_product:
        max_stat_product = stat_product
        best_combination = combination

print(best_combination, max_stat_product)