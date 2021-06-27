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

def pogostat_to_pvpoke(pokemon): # convert name from PogoStat.com to one usable in PVPoke.com
    if pokemon.endswith("Alola Form"):
        return pokemon.split()[0] + " (Alolan)"
    elif pokemon.endswith("Galarian Form"):
        return pokemon.split()[0] + " (Galarian)"
    elif pokemon.startswith("Wormadam"):
        return "Wormadam (" + (pokemon.split()[1] + ")" if ' ' in pokemon else "Plant)")
    elif pokemon.startswith("Castform"):
        return "Castform" + (" (" + pokemon.split()[1] + ")" if ' ' in pokemon else "&!Castform (")
    elif pokemon.startswith("Deoxys"):
        return "Deoxys" + (" (" + pokemon.split()[1] + ")" if ' ' in pokemon else "")
    elif pokemon.startswith("Giratina"):
        return "Giratina (Origin)" if ' ' in pokemon else "Giratina (Altered)"
    elif pokemon.startswith("Meowstic"):
        return "Meowstic (Female)" if ' ' in pokemon else "Meowstic (Male)"
    elif pokemon.startswith("Thundurus") or pokemon.startswith("Tornadus") or pokemon.startswith("Landorus"):
        return pokemon.split()[0] + (" (Therian)" if ' ' in pokemon else " (Incarnate)")
    elif pokemon.startswith("Rotom"):
        return "Rotom (" + pokemon.split()[1] + ")"
    elif pokemon.lower() in ["sandshrew", "sandslash", "grimer", "muk", "vulpix", "ninetales", "meowth", "persian", "exeggutor", "raichu", "marowak", "diglett", "dugtrio", "rattata", "raticate", "geodude", "graveler", "golem"]:
        return pokemon + "&!alolan"
    elif pokemon.lower() in ["ponyta", "rapidash", "meowth", "weezing", "zigzagoon", "linoone", "farfetch'd", "darumaka", "darmanitan", "stunfisk", "slowpoke", "slowbro", "mr. mime"]:
        return pokemon + "&!galarian"
    return pokemon

def get_rank_from_pvpoke(driver, pokemon_list):
    pokemons = []
    driver.get("https://pvpoke.com/rankings/all/" + str(max_cp) + "/overall/")
    search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "poke-search")))
    for pokemon_entry in pokemon_list:
        pokemon = pogostat_to_pvpoke(pokemon_entry[0])
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
    for pokemon in pokemons: # print all pokemon with ranks in a format that can be pasted as a table on Reddit
        print("| " + str(pokemon[0]) + " | " + pokemon[1] + " | " + str(pokemon[2]) + " |")
    print()

best_buddy = []
no_best_buddy = []
perfect_iv = []
pokemons = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata Alola Form", "Rattata", "Raticate Alola Form", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu Alola Form", "Raichu", "Sandshrew Alola Form", "Sandshrew", "Sandslash Alola Form", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix Alola Form", "Vulpix", "Ninetales Alola Form", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett Alola Form", "Diglett", "Dugtrio Alola Form", "Dugtrio", "Meowth Alola Form", "Meowth", "Meowth Galarian Form", "Persian Alola Form", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude Alola Form", "Geodude", "Graveler Alola Form", "Graveler", "Golem Alola Form", "Golem", "Ponyta Galarian Form", "Ponyta", "Rapidash Galarian Form", "Rapidash", "Slowpoke Galarian Form", "Slowpoke", "Slowbro Galarian Form", "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Farfetch'd Galarian Form", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer Alola Form", "Grimer", "Muk Alola Form", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor Alola Form", "Exeggutor", "Cubone", "Marowak Alola Form", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Weezing Galarian Form", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime Galarian Form", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Zigzagoon Galarian Form", "Linoone", "Linoone Galarian Form", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform Sunny Form", "Castform Snowy Form", "Castform Rainy Form", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys Speed Forme", "Deoxys Defense Forme", "Deoxys Attack Forme", "Deoxys", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam Trash Cloak", "Wormadam Sandy Cloak", "Wormadam", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom Wash Rotom", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran", "Regigigas", "Giratina Origin Forme", "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darumaka Galarian Form", "Darmanitan Galarian Form", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Stunfisk Galarian Form", "Mienfoo", "Mienshao", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Cobalion", "Terrakion", "Virizion", "Tornadus Therian Forme", "Tornadus", "Thundurus Therian Forme", "Thundurus", "Reshiram", "Zekrom", "Landorus Therian Forme", "Landorus", "Kyurem", "Genesect", "Chespin", "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox", "Froakie", "Frogadier", "Greninja", "Bunnelby", "Diggersby", "Fletchling", "Fletchinder", "Talonflame", "Litleo", "Pyroar", "Pancham", "Pangoro", "Espurr", "Meowstic Female", "Meowstic", "Spritzee", "Aromatisse", "Swirlix", "Slurpuff", "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher", "Clawitzer", "Sylveon", "Goomy", "Sliggoo", "Goodra", "Klefki", "Noibat", "Noivern", "Xerneas", "Yveltal", "Meltan", "Melmetal", "Obstagoon", "Perrserker", "Sirfetch’d", "Mr. Rime", "Runerigus"]

driver = webdriver.Firefox()
driver.get("https://pogostat.com")

pokelist = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "poke")))
button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@id='cp_cap']/following-sibling::button")))
max_lvl = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "max_lvl"))))
league = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cp_cap"))))
min_iv = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "min_iv"))))

league.select_by_value(str(max_cp))

for pokemon in pokemons:
    pokelist.clear()
    pokelist.send_keys(pokemon)
    if pokemon in ["Mew", "Celebi", "Jirachi", "Victini", "Darkrai", "Genesect", "Deoxys", "Deoxys Attack Forme", "Deoxys Defense Forme", "Deoxys Speed Forme"]:
        min_iv.select_by_value("10")
    elif pokemon in ["Zapdos", "Moltres", "Articuno", "Mewtwo", "Raikou", "Entei", "Suicune", "Lugia", "Ho-oh", "Regirock" ,"Regice", "Registeel", "Latios", "Latias", "Kyogre", "Groudon", "Rayquaza", "Dialga", "Palkia", "Heatran", "Regigigas", "Cresselia", "Giratina", "Giratina Origin Forme", "Cobalion", "Terrakion", "Virizion", "Tornadus Therian Forme", "Tornadus", "Thundurus Therian Forme", "Thundurus", "Landorus Therian Forme", "Landorus", "Reshiram", "Zekrom", "Kyurem", "Xerneas", "Yveltal"]:
        min_iv.select_by_value("1")
    else:
        min_iv.select_by_value("0")

    max_lvl.select_by_value("100") # setting level cap 51
    button.click()

    rank1_level_51 = float(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[5]"))).text)
    rank1_atk_51 = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[2]"))).text)
    rank1_def_51 = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[3]"))).text)
    rank1_hp_51 = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[4]"))).text)
    rank1_cp_51 = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[6]"))).text)

    max_lvl.select_by_value("98") # setting level cap 50
    button.click()

    rank1_level_50 = float(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[5]"))).text)
    rank1_atk_50 = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[2]"))).text)
    rank1_def_50 = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[3]"))).text)
    rank1_hp_50 = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[4]"))).text)
    rank1_cp_50 = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='output']/div[3]/div[6]"))).text)

    if rank1_atk_51 == 15 and rank1_def_51 == 15 and rank1_hp_51 > 13:
        if rank1_cp_51 >= min_cp or (max_cp == 1500 and pokemon in ["Wobbuffet"]):
            perfect_iv.append((pokemon, rank1_cp_51))
    elif rank1_atk_50 == 15 and rank1_def_50 == 15 and rank1_hp_50 > 13:
        if rank1_cp_50 >= min_cp:
            perfect_iv.append((pokemon, rank1_cp_50))
    elif rank1_level_51 > 50:
        best_buddy.append((pokemon, rank1_level_51))
    elif rank1_level_51 > 41:
        no_best_buddy.append((pokemon, rank1_level_51))

get_rank_from_pvpoke(driver, perfect_iv)
get_rank_from_pvpoke(driver, best_buddy)
get_rank_from_pvpoke(driver, no_best_buddy)

driver.close()