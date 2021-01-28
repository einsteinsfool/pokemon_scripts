from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
from math import ceil

type_color = {"bug": "#8cac31", "dark": "#2a2a29", "dragon": "#201480", "electric": "#fbd724", "fairy": "#ed1e79", "fighting": "#b5270c", "fire": "#e83e25", "flying": "#5e43d5", "ghost": "#2e31b5", "grass": "#39b54a", "ground": "#ed9006", "ice": "#65e2ff", "normal": "#c7b299", "poison": "#93279c", "psychic": "#ed1e79", "rock": "#a67c52", "steel": "#808080", "water": "#0084bc"}

driver = webdriver.Firefox()
driver.get("https://pvpoke.com/moves/fast")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//table)[2]/tr[69]")))

# get data about fast moves
fast_moves = {}
for row in driver.find_elements_by_xpath("(//table)[2]/tr[position()>1]"):
    fast_move = row.text.split('\n')
    fast_moves[fast_move[0]] = (int(fast_move[2].split()[1]), int(fast_move[2].split()[2]))

driver.get("https://pvpoke.com/moves/charged")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//table)[2]/tr[69]")))

# get data about charged moves
charged_moves = {}
for row in driver.find_elements_by_xpath("(//table)[2]/tr[position()>1]"):
    charged_move = row.text.split('\n')
    charged_moves[charged_move[0]] = (charged_move[1], int(charged_move[2].split()[1]))

driver.get("https://pvpoke.com/rankings")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'rankings-container')]/div[contains(@class, 'rank')][600]"))) # wait for the ranking to load
privacy_agreement_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ncmp__banner-btns')]/button[2]")))
privacy_agreement_button.click()

file = open("moves.html", "w")
file.write("<html>\n<head>\n<title>Pokemon moves</title>\n</head>\n<body>\n<table style='border-collapse: collapse; font-weight: bold'>")

for row in driver.find_elements_by_xpath("//div[contains(@class, 'rankings-container')]/div[contains(@class, 'rank')]"):
    pokemon = row.text.replace("\n†\n", "" if row.text[row.text.find('†')+2] == ',' else "\n").split('\n')
    name = re.sub("^#[0-9]+", "", pokemon[0])
    if "Shadow" in name or "XL" in name:
        continue
    fast_move, first_charged, second_charged = pokemon[1].replace("*", "").split(", ")
    if fast_move.startswith("Hidden"):
        fast_move = "Hidden Power"

    row.click() # click Pokemon entry to display all its charged moves
    charged_move_list = row.find_elements_by_xpath("div[contains(@class, 'details')]/div[6]/div[3]/div")

    file.write("<tr height='36' style='text-align: center; border: 3px solid'>")
    file.write("<td rowspan='" + str(len(charged_move_list)) + "' style='border: 3px solid'>" + name.upper())
    file.write("</td><td rowspan='" + str(len(charged_move_list)) + "'>" + fast_move.upper() + "</td>")

    is_first = True
    for charged_move in charged_move_list:
        charged_move_name = charged_move.find_element_by_xpath("div/span[2]").text.replace("*", "").replace("†", "")
        needed_fasts_for_charged = ceil(charged_moves[charged_move_name][1]/fast_moves[fast_move][0])

        if not is_first:
            file.write("<tr height='36' style='text-align: center; border: 3px solid'>")
        is_first = False
        file.write("<td style='border: 3px solid'>" + charged_move_name.upper() + "</td>")

        for i in range(42): # 42 is max possible no. turns to load a charged move
            file.write("<td width='36' style='color: white; font-size: 27px; ")
            if i < needed_fasts_for_charged * fast_moves[fast_move][1]:
                file.write("background-color: " + type_color[charged_moves[charged_move_name][0]])
                if (i+1) % fast_moves[fast_move][1] == 0:
                    file.write("; border-right: 3px solid black")
            else:
                file.write("border-right: 3px solid black")
            file.write("'>")
            if i == 0:
                file.write(str(needed_fasts_for_charged))
            elif (i+1 == needed_fasts_for_charged * fast_moves[fast_move][1] and
                    ceil(2.0*charged_moves[charged_move_name][1]/fast_moves[fast_move][0]) < 2*ceil(charged_moves[charged_move_name][1]/fast_moves[fast_move][0])):
                file.write("*")
            file.write("</td>")
        file.write("</tr>\n")

file.write("</table>\n</body>\n</html>")

driver.close()