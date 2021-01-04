import faster_than_requests as r
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

min_cp = 2271 # 1388 for Great League
max_cp = 2500 # 1500 for Great League

def get_rank_from_pvpoke(driver, pokemon_list):
    pokemons = []
    driver.get("https://pvpoke.com/rankings/all/" + str(max_cp) + "/overall/")
    search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "poke-search")))
    for pokemon_entry in pokemon_list:
        pokemon = pokemon_entry[0]
        if pokemon.endswith("Alola Form"):
            pokemon = pokemon.split()[0] + " (Alolan)"
        elif pokemon.endswith("Galarian Form"):
            pokemon = pokemon.split()[0] + " (Galarian)"
        elif pokemon.startswith("Wormadam"):
            pokemon = "Wormadam (" + (pokemon.split()[1] + ")" if ' ' in pokemon else "Plant)")
        elif pokemon.startswith("Castform"):
            pokemon = "Castform" + (" (" + pokemon.split()[1] + ")" if ' ' in pokemon else "")
        elif pokemon.startswith("Deoxys"):
            pokemon = "Deoxys" + (" (" + pokemon.split()[1] + ")" if ' ' in pokemon else "")
        elif pokemon.startswith("Giratina"):
            pokemon = "Giratina (Origin)" if ' ' in pokemon else "Giratina (Altered)"
        elif pokemon.lower() in ["sandshrew", "sandslash" "grimer", "muk", "vulpix", "ninetales", "exeggutor", "raichu", "marowak", "diglett", "dugtrio", "rattata", "raticate", "geodude", "graveler", "golem"]:
            pokemon += "&!alolan"
        elif pokemon.lower() in ["ponyta", "rapidash", "meowth", "persian", "weezing", "zigzagoon", "linoone", "farfetch'd", "darumaka", "darmanitan", "stunfisk"]:
            pokemon += "&!galarian"
        search.clear()
        search.send_keys(pokemon + "&!shadow")
        time.sleep(8)
        try:
            row = driver.find_element_by_xpath("//div[contains(@class, 'rankings-container')]/div[not(@style) or not(string-length(@style))]")
            pvpoke_rank = int(row.text[1] + (row.text[2] if row.text[2].isdigit() else '') + (row.text[3] if row.text[3].isdigit() else ''))
        except:
            pvpoke_rank = 999
        pokemons.append((pvpoke_rank, pokemon, pokemon_entry[1]))
    pokemons = sorted(pokemons)
    for pokemon in pokemons:
        print("| " + str(pokemon[0]) + " | " + pokemon[1] + " | " + str(pokemon[2]) + " |")
    print()
#    print(sorted(pokemons))

pokemons = []
best_buddy = []
no_best_buddy = []
perfect_iv = []

source = r.get2str("https://pogostat.com/pokedex.js")

index = source.find('"name"')
while index > 0:
    pokemon = source[index+9:source.find('"', index+9)]
    pokemons.append(pokemon)
    index = source.find('"name"', index+9)

driver = webdriver.Firefox()
driver.get("https://pogostat.com")

pokelist = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "poke")))
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@id='cp_cap']/following-sibling::button")))
max_lvl = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "max_lvl"))))
league = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cp_cap"))))
min_iv = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "min_iv"))))

max_lvl.select_by_value("100")
league.select_by_value(str(max_cp))

for pokemon in pokemons:
    if pokemon in ["Frillish", "Skiddo", "Spritzee", "Pumpkaboo Super Size", "Pumpkaboo Large Size", "Pumpkaboo", "Bergmite", "Honedge", "Amaura", "Carbink", "Mienfoo", "Larvesta", "Floette", "Pancham", "Aegislash", "Furfrou", "Kecleon", "Phione", "Sliggoo"]:
        continue
    pokelist.clear()
    pokelist.send_keys(pokemon)
    if pokemon in ["Mew", "Celebi", "Jirachi", "Victini", "Darkrai", "Genesect", "Deoxys", "Deoxys Attack Forme", "Deoxys Defense Forme", "Deoxys Speed Forme"]:
        min_iv.select_by_value("10")
    elif pokemon in ["Zapdos", "Moltres", "Articuno", "Mewtwo", "Raikou", "Entei", "Suicune", "Lugia", "Ho-oh", "Regirock" ,"Regice", "Registeel", "Latios", "Latias", "Kyogre", "Groudon", "Rayquaza", "Dialga", "Palkia", "Heatran", "Regigigas", "Cresselia", "Giratina", "Giratina Origin Forme", "Cobalion", "Terrakion", "Virizion", "Thundurus", "Tornadus", "Landorus", "Reshiram", "Zekrom", "Kyurem"]:
        min_iv.select_by_value("1")
    else:
        min_iv.select_by_value("0")
    button.click()

    rank1_level = float(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[5]"))).text)
    rank1_atk = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[2]"))).text)
    rank1_def = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[3]"))).text)
    rank1_hp = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[4]"))).text)
    rank1_cp = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[6]"))).text)

    if rank1_atk == 15 and rank1_def == 15 and rank1_hp > 13:
        if rank1_cp >= min_cp or (max_cp == 1500 and pokemon in ["Wobbuffet"]):
            perfect_iv.append((pokemon, rank1_cp))
    elif rank1_level > 50:
        best_buddy.append((pokemon, rank1_level))
    elif rank1_level > 41:
        no_best_buddy.append((pokemon, rank1_level))

get_rank_from_pvpoke(driver, perfect_iv)
get_rank_from_pvpoke(driver, best_buddy)
get_rank_from_pvpoke(driver, no_best_buddy)

driver.close()