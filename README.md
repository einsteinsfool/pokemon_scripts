# Pokemon scripts
Scripts I wrote (usually in Python) that help me in Pokemon GO.

## pokemon_needing_XL_candy.py
Downloads list of Pokemon (from [here](https://pogostat.com/pokedex.js)). For each of these Pokemon script checks rank1 for PVP in either Great or Ultra League (depending on `max_cp` variable) and determines if it requires powering up with XL candy (meaning level 41.5+). If it does, the Pokemon is saved in an appropriate array:
- `perfect_iv`: for 15/15/15 Pokemon above `min_cp` CP
- `best_buddy`: for Pokemon that need best buddy for rank1 (without stats 15/15/15)
- `no_best_buddy`: for Pokemon that don't need best buddy for rank1

Then, for each array, Pokemon PvPoke rank is checked (in Great or Ultra League depending on `max_cp` variable) and sorted by that rank Pokemon are printed.

Thanks to this script we can get all Pokemon that need XL candy for Great and Ultra Leagues and see which of them are worth powering up. We can also use it to choose perfect IV Pokemon to max for Ultra League if we don't want to use dust on Pokemon useless outside of Ultra League.

## discord_injecter.py
Used for Discord bot that notifies about specific Pokemon. Commands from [Pastebin](https://pastebin.com/raw/jr5qpQEm) notify about rare Pokemon, perfect IV Pokemon, Pokemon that don't spawn in the wild (just in case Niantic changes something) and rank1 Pokemon for PVP Great League. Each command needs to be entered in Discord in a separate message, so it's boring to paste over 600 commands by hand (especially if bot breaks and all commands need to be sent again).

This script downloads the list of commands. Logs in to Discord (manual entering of 2FA code is needed if enabled). Switches to chat with Pokemon notification bot. Sends each command in a separate message. Waits 3 seconds for the bot to process the request.

## stats.py
When farming stardust by catching a lot of Pokemon, it's nice to listen to audiobooks or have a companion to kill boredom. Sometimes conversation with the companion fades and that's why I like to have some trivia questions. To find as many question as possible I wrote this script. It gathers some statistics, like:
- palindrome Pokemon
- Pokemon starting/ending with each letter
- Pokemon starting with each two letters
- substring of length 4 that occurrs in the most Pokemon names
- Pokemon with the shortest/longest name
- Pokemon with 3+ consecutive vowels
- Pokemon with most/least vowels
- Pokemon with the same statistics (attack, defense, stamina) but not just different forms of the same species (e.g. Muk, alolan Muk)
- Pokemon with the highest attack/defense/stamina that is not the last evolution
- Pokemon with highest attack/defense/stamina/tankiness (tankiness=defense\*stamina)

## great_league_rayquaza_combinations.py
Pokemon from raids are on level 20. Most legendaries on that level are above 1500 CP limit for any IV. For level 15 (obtainable from research), though, most of them fit in the Great League limit, especially when trading them with Good Friends as the bottom IV is then 1/1/1. This script calculates how likely it is to get a Great League legendary from a trade, by checking all possible IVs on that level (default 15) and counting the ones that result in CP up to 1500.

It also checks stat product for each possible combination because [PogoStat](https://pogostat.com) doesn't have the option to set floor level and displays only IVs for legendary below level 15 which is the lowest obtainable level, so you can't check what is it's best obtainable IV for Great League. Finally, it chooses the combination with the highest stat product and prints it. It was only after coding that I learned about [PVP IVs](https://pvpivs.com) which makes this functionality redundant, so I added an option to skip this part and save time.
