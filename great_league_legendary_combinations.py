from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import re
import sys

pokemon_name = "Rayquaza" # other good names: Zapdos, Lugia, Ho-Oh, Latios, Latias
find_rank1 = True # decide if you want to find legendary's rank1 for Great League

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get("https://pokemon.gameinfo.io/en/tools/cp-calculator")

pokemon = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "vs__search")))
level, attack, defense, stamina = driver.find_elements_by_xpath("//input[@type='number']")

# necessary because of bad sorting on GameInfo; check next Pokemon in combobox until a match
down_key_presses = 0
while True:
    pokemon.send_keys(pokemon_name)
    for i in range(down_key_presses):
        pokemon.send_keys(Keys.ARROW_DOWN)
    pokemon.send_keys(Keys.RETURN)
    check_correct = driver.find_element_by_xpath("//div[@class='pokemon']/a").text
    if check_correct == pokemon_name:
        break
    down_key_presses += 1

level.clear()
level.send_keys("15") # level 15 because it's from a research; change to 20 for raids/eggs

start_index = 1 # 0 for no friendship (not possible to trade legendaries), 1 for Good Friends, 2 for Great Friends, 3 for Ultra Friends, 5 for Best Friends, 12 for Lucky Friends
combinations = []
lucky_combinations = 0
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
                if a >= 12 and d >= 12 and s >= 12:
                    lucky_combinations += 1

print("%d/%d combinations = %.2f%%" % (len(combinations), (16-start_index)**3, 100*len(combinations)/(16-start_index)**3))
print("%d/64 lucky combinations = %.2f%%" % (lucky_combinations, 100*lucky_combinations/64))
print("Overall probability = %.2f%%" % ((95*len(combinations)/(16-start_index)**3) + 5*lucky_combinations/64))

if find_rank1 == False:
    sys.exit()

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

print('/'.join(map(str, best_combination)), max_stat_product)

driver.close()