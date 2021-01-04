# Pokemon scripts
Scripts I wrote (usually in Python) that help me in Pokemon GO.

## pokemon_needing_XL_candy.py
Downloads list of Pokemon (from [here](https://pogostat.com/pokedex.js)). For each of these Pokemon script checks rank1 for PVP in either Great or Ultra League (depending on `max_cp` variable) and determines if it requires powering up with XL candy (meaning level 41.5+). If it does, the Pokemon is saved in an appropriate array:
- `perfect_iv`: for 15/15/15 Pokemon above `min_cp` CP
- `best_buddy`: for Pokemon that need best buddy for rank1 (without stats 15/15/15)
- `no_best_buddy`: for Pokemon that don't need best buddy for rank1

Then, for each array, Pokemon PvPoke rank is checked (in Great or Ultra League depending on `max_cp` variable) and sorted by that rank Pokemon are printed.

Thanks to this script we can get all Pokemon that need XL candy for Great and Ultra Leagues and see which of them are worth powering up. We can also use it to choose perfect IV Pokemon to max for Ultra League if we don't want to use dust on Pokemon useless outside of Ultra League.
